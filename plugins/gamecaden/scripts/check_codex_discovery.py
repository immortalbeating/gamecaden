"""Probe a fresh Codex app-server against an explicitly selected local installation."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import subprocess
import threading

EXPECTED = {"flow", "init", "brainstorm", "design", "develop", "assets", "verify", "close"}


def probe(codex, codex_home, project_root):
    environment = {**os.environ, "CODEX_HOME": str(Path(codex_home).absolute())}
    process = subprocess.Popen([codex, "app-server", "--stdio"], env=environment, cwd=project_root,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, encoding="utf-8", creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    received = queue.Queue()
    def read():
        for line in process.stdout:
            try:
                received.put(json.loads(line))
            except ValueError:
                pass
        received.put({"closed": True})
    threading.Thread(target=read, daemon=True).start()
    # Drain diagnostics without exposing credentials or allowing a filled stderr pipe to block.
    threading.Thread(target=lambda: list(process.stderr), daemon=True).start()
    counter = 0
    def request(method, params):
        nonlocal counter
        counter += 1
        process.stdin.write(json.dumps({"id": counter, "method": method, "params": params}) + "\n")
        process.stdin.flush()
        while True:
            response = received.get(timeout=30)
            if response.get("closed"):
                raise RuntimeError("app-server closed before response")
            if response.get("id") == counter:
                if "error" in response:
                    raise RuntimeError(f"{method}: {response['error']}")
                return response["result"]
    try:
        initialized = request("initialize", {"clientInfo": {"name": "gamecaden-discovery", "version": "1.0"},
                                             "capabilities": {"experimentalApi": True}})
        process.stdin.write('{"method":"initialized","params":{}}\n')
        process.stdin.flush()
        listing = request("skills/list", {"cwds": [str(Path(project_root).absolute())], "forceReload": True})
        skills = []
        for group in listing.get("data", []):
            for skill in group.get("skills", []):
                path = str(skill.get("path", ""))
                if re.search(r"/plugins/cache/[^/]+/gamecaden/[^/]+/skills/", path.replace("\\", "/")):
                    data = Path(path).read_bytes()
                    skills.append({"name": skill["name"], "path": path, "sha256": hashlib.sha256(data).hexdigest(),
                                   "enabled": skill.get("enabled", True), "description": skill.get("description")})
        names = {item["name"].rsplit(":", 1)[-1] for item in skills}
        if names != EXPECTED or len(skills) != 8 or not all(item["enabled"] for item in skills):
            raise RuntimeError(f"Expected eight enabled Gamecaden skills, found {sorted(names)}")
        return {"status": "ok", "initialized": initialized, "skills": skills,
                "fresh_process": True, "model_turn_executed": False}
    finally:
        process.stdin.close()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", required=True, help="Exact Codex executable")
    parser.add_argument("--codex-home", required=True, help="Explicit home, preferably an isolated probe installation")
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = probe(args.codex, args.codex_home, args.project_root)
    except (OSError, RuntimeError, queue.Empty, ValueError) as error:
        result = {"status": "rejected", "error": str(error)}
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "skill_count": len(result.get("skills", [])), "output": args.output}, ensure_ascii=False))
    return 0 if result["status"] == "ok" else 2


if __name__ == "__main__":
    raise SystemExit(main())
