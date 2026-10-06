"""Loopback panel host. Source files and Workflow receipts remain authoritative."""
from __future__ import annotations

import argparse
import base64
import copy
import csv
import ctypes
import hashlib
import hmac
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import tempfile
import threading
import time
from urllib.parse import parse_qs, unquote, urlsplit
import uuid

from workflow_formats import WorkflowError, canonical, json_load, request_digest, rebase
from workflow_io import Workflow, now
from workflow_panel_data import PanelData, PanelDataError
from workflow_governance import Governance

MAX_BODY = 1024 * 1024
FRONTEND = Path(__file__).resolve().parents[1] / "panels/night"
CAPS = {"task_body_write": "task_body", "decision_record": "decisions", "asset_selection": "asset_selection"}


def fail(code, message, status=400):
    raise PanelDataError(code, message, status)


def fields(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys() or value.keys() - set(required) - set(optional):
        fail("invalid_request", "请求字段与此动作不匹配")


def string(value, name, maximum=300, empty=False):
    if not isinstance(value, str) or len(value) > maximum or (not empty and not value.strip()):
        fail("invalid_request", f"{name} 必须是有效文本，最长 {maximum} 字符")
    return value


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,119}", value):
        fail("invalid_request", "无效的 request_id 或项目 id")
    return value


class Signer:
    """Persistent host key: tickets freeze a snapshot, never grant a session/capability."""
    def __init__(self, state_dir):
        folder = Path(state_dir).absolute() / "private"
        folder.mkdir(parents=True, exist_ok=True)
        if folder.is_symlink() or (hasattr(folder, "is_junction") and folder.is_junction()):
            fail("invalid_host", "宿主状态目录不能是链接")
        # Secrets go into a dedicated directory, never a shared artifact directory.
        if os.name == "nt":
            from ctypes import wintypes
            output = subprocess.check_output([str(Path(os.environ["SystemRoot"]) / "System32/whoami.exe"),
                                              "/user", "/fo", "csv", "/nh"], creationflags=subprocess.CREATE_NO_WINDOW)
            sid = list(csv.reader(output.decode("utf-8", errors="replace").splitlines()))[0][-1]
            if not re.fullmatch(r"S-1-[0-9-]+", sid):
                fail("invalid_host", "无法确定本机启动身份")
            advapi = ctypes.WinDLL("advapi32", use_last_error=True)
            kernel = ctypes.WinDLL("kernel32", use_last_error=True)
            convert = advapi.ConvertStringSecurityDescriptorToSecurityDescriptorW
            convert.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.DWORD)]
            convert.restype = wintypes.BOOL
            apply = advapi.SetFileSecurityW
            apply.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_void_p]
            apply.restype = wintypes.BOOL
            kernel.LocalFree.argtypes = [ctypes.c_void_p]
            kernel.LocalFree.restype = ctypes.c_void_p
            descriptor = ctypes.c_void_p()
            sddl = f"D:P(A;OICI;FA;;;{sid})(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)"
            if not convert(sddl, 1, ctypes.byref(descriptor), None):
                raise ctypes.WinError(ctypes.get_last_error())
            try:
                if not apply(str(folder), 0x80000004, descriptor):  # protected DACL only; no SACL/privilege change
                    raise ctypes.WinError(ctypes.get_last_error())
            finally:
                kernel.LocalFree(descriptor)
        else:
            folder.chmod(0o700)
        self.folder = folder
        path = folder / "ticket-key"
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            if path.is_symlink():
                fail("invalid_host", "签名密钥不能是链接")
        else:
            with os.fdopen(fd, "wb") as stream:
                stream.write(secrets.token_bytes(32))
        self.key = path.read_bytes()
        if len(self.key) != 32:
            fail("invalid_host", "签名密钥格式无效")

    def sign(self, payload):
        data = canonical(payload).encode("utf-8")
        signature = hmac.new(self.key, data, hashlib.sha256).digest()
        return base64.urlsafe_b64encode(data).decode().rstrip("=") + "." + signature.hex()

    def read(self, token):
        string(token, "ticket", 24000)
        try:
            encoded, signature = token.split(".")
            data = base64.b64decode(encoded + "=" * (-len(encoded) % 4), altchars=b"-_", validate=True)
            expected = hmac.new(self.key, data, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected):
                raise ValueError()
            payload = json_load(data.decode("utf-8"))
            if not isinstance(payload, dict):
                raise ValueError()
            return payload
        except (ValueError, UnicodeError):
            fail("invalid_ticket", "操作快照无效，请重新读取来源", 403)


class Binding:
    def __init__(self, config, signer):
        fields(config, ("id", "root"), ("name", "workspace", "external_sources", "write", "reviewer", "identity_source"))
        self.id = identifier(config["id"])
        self.data = PanelData(config["root"], workspace=config.get("workspace"),
                              external_sources=config.get("external_sources"), name=config.get("name"), project_id=self.id)
        self.kind = "external" if self.data.external_sources else "native"
        write = config.get("write", {})
        if not isinstance(write, dict) or write.keys() - set(CAPS.values()) or any(type(v) is not bool for v in write.values()):
            fail("invalid_host", "write 必须是明确的动作开关")
        self.caps = {k: self.kind == "native" and write.get(v, False) for k, v in CAPS.items()}
        self.actor = config.get("reviewer")
        if self.actor is not None:
            fields(self.actor, ("kind", "id"))
            if self.actor["kind"] not in ("tool", "agent", "user"):
                fail("invalid_host", "未知记录者类型")
            string(self.actor["id"], "actor.id", 120)
        if any(self.caps.values()) and self.actor is None:
            fail("invalid_host", "写入需要启动方绑定记录者身份")
        self.identity_source = config.get("identity_source", "local-launch" if self.actor else "read-only")
        self.signer = signer
        self.lock = threading.RLock()
        self.active_digest = None
        self.workflow = Workflow(self.data.root, actor=self.actor, decision_authorizer=self.authorize)
        identity = {**config, "root": str(self.data.root)}
        self.binding_id = hashlib.sha256(canonical(identity).encode("utf-8")).hexdigest()

    def info(self):
        return {"id": self.id, "name": self.data.name or self.data.root.name, "root": str(self.data.root),
                "kind": self.kind, "binding_id": self.binding_id, "capabilities": self.caps,
                "actor": self.actor, "identity_source": self.identity_source}

    def authorize(self, event, request):
        # Only the exact request being submitted through this bound session may claim user.
        return (self.active_digest is not None and self.caps["decision_record"]
                and event["actor"] == self.actor and request_digest(request) == self.active_digest)

    def require(self, capability):
        if not self.caps[capability]:
            fail("read_only", "此来源未开启该写入动作", 403)

    def context(self):
        context = {"project_root": str(self.data.root), "base_dir": str(self.data.root)}
        if self.data.workspace:
            context["workspace"] = str(self.data.workspace)
        return context

    def envelope(self, operation, payload, rid=None):
        return {"protocol_version": 1, "request_id": rid or uuid.uuid4().hex, "operation": operation,
                "context": self.context(), "payload": payload}

    def freeze(self, kind, facts):
        preview = {"type": kind, "project_id": self.id, "binding_id": self.binding_id,
                   "actor": self.actor, "issued_at": now(), **facts}
        return {"ticket": self.signer.sign(preview), "preview": preview}

    def thaw(self, token, kind):
        facts = self.signer.read(token)
        if facts.get("type") != kind or facts.get("binding_id") != self.binding_id or facts.get("actor") != self.actor:
            fail("invalid_ticket", "快照不属于当前项目、身份或动作", 403)
        return facts

    def prepare_task(self, body):
        self.require("task_body_write")
        fields(body, ("key", "revision"))
        record = self.data.read(string(body["key"], "key"))
        if record["record_type"] != "task" or record["interpretation"] != "native" or "record.update" not in record["capabilities"]:
            fail("read_only", "只有可写原生 Task 正文可编辑", 403)
        if record["revision"] != body["revision"]:
            fail("revision_conflict", "正文来源已变化，输入会保留；请重新读取后核对", 409)
        return self.freeze("task", {"key": body["key"], "target": record["ref"], "path": record["path"],
                                    "title": record["title"], "source_revision": record["revision"]})

    def prepare_candidate(self, body, kind):
        self.require("decision_record" if kind == "review" else "asset_selection")
        required = ("asset_key", "candidate_id", "expected_revision", "expected_version")
        fields(body, required + (("scope",) if kind == "review" else ("use_id",)),
               ("use_id",) if kind == "review" else ())
        candidate = self.data.candidate(string(body["asset_key"], "asset_key"),
                                        string(body["candidate_id"], "candidate_id"))
        if candidate["ledger_revision"] != body["expected_revision"] or candidate["version"] != body["expected_version"]:
            fail("revision_conflict", "资产来源或候选版本已变化，不能以新版本替代当前预览", 409)
        if candidate["check"]["status"] != "verified":
            fail("candidate_invalid", "候选内容校验未通过，不能提交本次当前版本操作", 409)
        use_id = body.get("use_id")
        use = None
        if use_id:
            string(use_id, "use_id")
            use = next((u for u in candidate["all_uses"] if u["use_id"] == use_id), None)
            if use is None:
                fail("invalid_scope", "用途必须来自已登记的用途")
        if kind == "selection" and use is None:
            fail("invalid_scope", "指定候选需要已有用途")
        if use is not None:
            guard = self.data._project()
            use = rebase(use, Path(candidate["reference_base"]), self.data.root, guard.path)
        scope = string(body["scope"], "scope", 500) if kind == "review" else "既有用途候选指定"
        version = copy.deepcopy(candidate["version"])
        version["proof"] = {"path": candidate["manifest_path"]}
        subject = {"ref": candidate["asset_ref"], "candidate_id": candidate["candidate_id"],
                   "version": version, "scope": scope}
        if use is not None:
            subject["use"] = {k: use[k] for k in ("runtime_id", "consumer", "purpose", "baseline")}
        return self.freeze(kind, {"asset_id": candidate["asset_id"], "asset_key": body["asset_key"],
                                  "subject": subject, "use_id": use_id, "previous_use": use,
                                  "ledger_path": candidate["ledger_path"],
                                  "source_revision": candidate["ledger_revision"]})

    def commit(self, body, kind):
        cap = {"task": "task_body_write", "review": "decision_record", "selection": "asset_selection"}[kind]
        self.require(cap)
        fields(body, ("ticket", "request_id") + (("body",) if kind == "task" else ("conclusion", "note") if kind == "review" else ()))
        facts = self.thaw(body["ticket"], kind)
        rid = identifier(body["request_id"])
        if kind == "task":
            payload = {"target": facts["target"], "body": string(body["body"], "body", 700000, empty=True),
                       "reason": "通过已绑定本地面板保存 Task 正文"}
            request = self.envelope("record.update", payload, rid)
            condition_path = facts["path"]
        elif kind == "review":
            if body["conclusion"] not in ("accept", "revise", "reject"):
                fail("invalid_request", "结论须为 accept、revise 或 reject；暂缓保留在草稿")
            note = string(body["note"], "note", 8000)
            event = {"event_id": "panel-" + rid, "actor": self.actor, "action": body["conclusion"],
                     "subjects": [facts["subject"]], "scope": facts["subject"]["scope"],
                     "conclusion": note, "decided_at": None, "recorded_at": facts["issued_at"]}
            request = self.envelope("decision.record",
                                    {"title": facts["asset_id"] + " / " + facts["subject"]["candidate_id"] + " · " + facts["subject"]["scope"],
                                     "event": event}, rid)
            request["expected_subjects"] = [facts["subject"]]
            condition_path = facts["ledger_path"]
        else:
            use = copy.deepcopy(facts["previous_use"])
            use["candidate_id"] = facts["subject"]["candidate_id"]
            # Existing acceptance/evidence do not transfer to a different candidate.
            if use["candidate_id"] != facts["previous_use"]["candidate_id"]:
                use.pop("decision_refs", None)
                use.pop("evidence_refs", None)
            request = self.envelope("asset.select",
                                    {"ledger": {"path": facts["ledger_path"]}, "asset_id": facts["asset_id"],
                                     "action": "set", "use": use, "reason": "通过本地面板为既有用途指定候选"}, rid)
            request["expected_subjects"] = [facts["subject"]]
            condition_path = facts["ledger_path"]
        request["preconditions"] = [{"target": {"path": condition_path}, "expected_revision": facts["source_revision"]}]
        self.active_digest = request_digest(request)
        try:
            result = self.workflow.execute(request)
        finally:
            self.active_digest = None
        response = {"result": result, "record": None}
        if result.get("data", {}).get("ref"):
            readback = self.workflow.execute(self.envelope("record.read", {"target": result["data"]["ref"]}))
            if readback["status"] == "ok":
                response["record"] = readback["data"]
            else:
                response["readback_error"] = readback["errors"]
        return response

    def post(self, action, body):
        with self.lock:
            if action == "task/prepare":
                return self.prepare_task(body)
            if action in ("review/prepare", "selection/prepare"):
                return self.prepare_candidate(body, action.split("/")[0])
            if action in ("task/save", "review/commit", "selection/commit"):
                return self.commit(body, action.split("/")[0])
            if action == "operation/status":
                fields(body, ("request_id",))
                rid = identifier(body["request_id"])
                return {"result": self.workflow.execute(self.envelope("operation.status", {"request_id": rid}))}
            fail("not_found", "未知面板动作", 404)


class PanelHost:
    def __init__(self, config, state_dir):
        fields(config, ("version", "projects"), ("default_project_id",))
        if config["version"] != 1 or not isinstance(config["projects"], list) or not config["projects"]:
            fail("invalid_host", "宿主配置需要 version=1 和项目列表")
        self.signer = Signer(state_dir)
        self.projects = {}
        for item in config["projects"]:
            binding = Binding(item, self.signer)
            if binding.id in self.projects:
                fail("invalid_host", "项目 id 重复")
            self.projects[binding.id] = binding
        self.default_project = config.get("default_project_id", next(iter(self.projects)))
        if self.default_project not in self.projects:
            fail("invalid_host", "默认项目未注册")
        self.bootstrap = secrets.token_urlsafe(32)
        self.cookie_name = "workflow_" + secrets.token_hex(8)
        self.sessions = {}
        self.lock = threading.Lock()
        self.origin = None

    def connect(self, token):
        with self.lock:
            if self.bootstrap is None or not isinstance(token, str) or not hmac.compare_digest(self.bootstrap, token):
                fail("authentication_required", "启动连接已使用或失效，请从宿主获取新连接", 401)
            self.bootstrap = None
            session = {"id": secrets.token_urlsafe(32), "csrf": secrets.token_urlsafe(32),
                       "expires": time.time() + 12 * 3600}
            self.sessions[session["id"]] = session
            return session

    def session(self, cookies):
        cookie = SimpleCookie()
        try:
            cookie.load(cookies or "")
            value = cookie.get(self.cookie_name)
        except Exception:
            value = None
        session = self.sessions.get(value.value if value else "")
        if session is None or session["expires"] < time.time():
            fail("authentication_required", "请通过本机宿主启动连接", 401)
        return session

    def session_info(self, session):
        return {"session": {"id": hashlib.sha256(session["id"].encode()).hexdigest()[:16]},
                "csrf_token": session["csrf"], "projects": [p.info() for p in self.projects.values()],
                "default_project_id": self.default_project}

    def project(self, pid):
        try:
            return self.projects[pid]
        except KeyError:
            fail("not_found", "项目未注册", 404)


class Handler(BaseHTTPRequestHandler):
    server_version = "WorkflowPanel/1"
    sys_version = ""
    protocol_version = "HTTP/1.0"

    def setup(self):
        super().setup()
        self.connection.settimeout(8)

    def log_message(self, format, *args):
        # No token, cookie, raw path, document body, or user input in request logs.
        pass

    @property
    def host(self):
        return self.server.host

    def send(self, status, data, mime="application/json; charset=utf-8", headers=None):
        if not isinstance(data, bytes):
            data = json.dumps(data, ensure_ascii=False, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; media-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'none'")
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(data)

    def check_origin(self, mutation=False):
        if self.headers.get("Host") != urlsplit(self.host.origin).netloc:
            fail("invalid_host", "Host 不属于本机面板", 403)
        origin = self.headers.get("Origin")
        if (mutation and origin != self.host.origin) or (origin is not None and origin != self.host.origin):
            fail("cross_origin", "只允许本面板来源", 403)
        if self.headers.get("Sec-Fetch-Site") == "cross-site":
            fail("cross_origin", "不允许跨站请求", 403)

    def body(self):
        if self.headers.get_content_type() != "application/json" or self.headers.get("Transfer-Encoding"):
            fail("invalid_request", "请求须为有界 JSON", 415)
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            length = -1
        if not 0 <= length <= MAX_BODY:
            fail("request_too_large", "请求超过限制或缺少长度", 413)
        try:
            return json_load(self.rfile.read(length).decode("utf-8"))
        except (ValueError, UnicodeError, WorkflowError):
            fail("invalid_request", "JSON 内容无效")

    def route(self, method):
        self.check_origin(method == "POST")
        url = urlsplit(self.path)
        path = url.path
        if method == "GET" and not path.startswith("/api/"):
            public = {"/": ("index.html", "text/html; charset=utf-8"), "/index.html": ("index.html", "text/html; charset=utf-8"),
                      "/app.mjs": ("app.mjs", "text/javascript; charset=utf-8"), "/app.css": ("app.css", "text/css; charset=utf-8"), "/relations.mjs": ("relations.mjs", "text/javascript; charset=utf-8"), "/relations.css": ("relations.css", "text/css; charset=utf-8"),
                      "/panel-refresh.mjs": ("panel-refresh.mjs", "text/javascript; charset=utf-8"),
                      "/domain-reader.mjs": ("domain-reader.mjs", "text/javascript; charset=utf-8"),
                      "/relation-layout.mjs": ("relation-layout.mjs", "text/javascript; charset=utf-8"), "/vendor/elk.bundled.js": ("vendor/elk.bundled.js", "text/javascript; charset=utf-8")}
            if path not in public:
                fail("not_found", "文件未注册", 404)
            name, mime = public[path]
            return self.send(200, (FRONTEND / name).read_bytes(), mime)
        body = self.body() if method == "POST" else None
        if method == "POST" and path == "/api/connect":
            fields(body, ("token",))
            session = self.host.connect(body["token"])
            return self.send(200, self.host.session_info(session),
                             headers={"Set-Cookie": self.host.cookie_name + "=" + session["id"] + "; Path=/api/; HttpOnly; SameSite=Strict; Max-Age=43200"})
        session = self.host.session(self.headers.get("Cookie"))
        if method == "POST" and not hmac.compare_digest(self.headers.get("X-CSRF-Token", ""), session["csrf"]):
            fail("csrf_required", "缺少当前会话请求令牌", 403)
        if method == "GET" and path == "/api/session":
            return self.send(200, self.host.session_info(session))
        parts = path.split("/")
        if len(parts) < 5 or parts[1:3] != ["api", "projects"]:
            fail("not_found", "未知接口", 404)
        binding = self.host.project(unquote(parts[3]))
        action = "/".join(parts[4:])
        if method == "POST":
            return self.send(200, binding.post(action, body))
        with binding.lock:
            if action == "revisions":
                if url.query:
                    fail("invalid_request", "Version checks do not accept query parameters")
                return self.send(200, binding.data.revisions())
            if action == "governance":
                query = parse_qs(url.query)
                if query.keys() - {"focus"}:
                    fail("invalid_request", "未知治理视图参数")
                return self.send(200, Governance(binding.data).build(query.get("focus", [None])[0]))
            if action == "snapshot":
                query = parse_qs(url.query)
                if query.keys() - {"cursor", "limit"}:
                    fail("invalid_request", "未知查询参数")
                try:
                    limit = int(query.get("limit", ["100"])[0])
                except ValueError:
                    fail("invalid_request", "limit 无效")
                return self.send(200, binding.data.snapshot(query.get("cursor", [None])[0], limit))
            if len(parts) == 6 and parts[4] == "records":
                return self.send(200, binding.data.read(unquote(parts[5])))
            if len(parts) == 7 and parts[4] == "candidates":
                return self.send(200, binding.data.candidate(unquote(parts[5]), unquote(parts[6])))
            if len(parts) == 6 and parts[4] == "media":
                item = binding.data.media(unquote(parts[5]))
                data, mime = item["data"], item["mime"]
                headers = {"ETag": '"' + item["revision"] + '"', "Accept-Ranges": "bytes"}
                requested_range = self.headers.get("Range")
                if requested_range:
                    match = re.fullmatch(r"bytes=(\d*)-(\d*)", requested_range)
                    if not match or not any(match.groups()):
                        fail("invalid_range", "只支持单段媒体范围", 416)
                    left, right = match.groups()
                    start = int(left) if left else max(0, len(data) - int(right))
                    end = min(int(right), len(data)-1) if left and right else len(data)-1
                    if not 0 <= start <= end < len(data):
                        fail("invalid_range", "媒体范围超出内容", 416)
                    headers["Content-Range"] = f"bytes {start}-{end}/{len(data)}"
                    return self.send(206, data[start:end+1], mime, headers)
                return self.send(200, data, mime, headers)
        fail("not_found", "未知接口", 404)

    def handle_method(self, method):
        try:
            self.route(method)
        except PanelDataError as exc:
            self.send(exc.status, {"error": {"code": exc.code, "message": exc.message, "details": exc.details}})
        except (BrokenPipeError, ConnectionResetError, TimeoutError):
            pass
        except Exception:
            self.send(500, {"error": {"code": "internal_error", "message": "读取或操作失败；保留原请求并查询回执"}})

    def do_GET(self):
        self.handle_method("GET")

    def do_POST(self):
        self.handle_method("POST")

    def do_OPTIONS(self):
        self.send(403, {"error": {"code": "cross_origin", "message": "不开放跨来源接口"}})


def create_server(config, state_dir, port=8875):
    host = PanelHost(config, state_dir)
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.daemon_threads = True
    server.host = host
    host.origin = "http://127.0.0.1:" + str(server.server_port)
    return server


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--state-dir", required=True, help="Local host state, outside business records")
    parser.add_argument("--port", type=int, default=8875)
    parser.add_argument("--connection-file", help="Private file holding one-use bootstrap URL")
    args = parser.parse_args()
    config = json_load(Path(args.config).read_text(encoding="utf-8-sig"))
    server = create_server(config, args.state_dir, args.port)
    connection = Path(args.connection_file).absolute() if args.connection_file else server.host.signer.folder / "connection.json"
    if connection.parent != server.host.signer.folder or connection.is_symlink():
        fail("invalid_host", "连接文件必须直接放在宿主 state-dir/private 目录")
    fd, temporary = tempfile.mkstemp(prefix="connection-", suffix=".tmp", dir=server.host.signer.folder)
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump({"url": server.host.origin + "/#connect=" + server.host.bootstrap,
                   "origin": server.host.origin, "pid": os.getpid()}, stream)
    os.replace(temporary, connection)
    print("Local panel listening at " + server.host.origin, flush=True)
    try:
        server.serve_forever(poll_interval=0.3)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
