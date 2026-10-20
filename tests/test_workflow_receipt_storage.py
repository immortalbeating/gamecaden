"""Lossless settled-receipt storage checks using disposable projects."""
import base64
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import unittest
from unittest.mock import patch

import test_workflow_io as integration
from workflow_formats import WorkflowError
from workflow_io import Workflow
from workflow_storage import Store, filesystem_path, receipt_bytes
import workflow_storage as storage


class ReceiptStorage(unittest.TestCase):
    setUp = integration.Integration.setUp
    request = integration.Integration.request
    condition = integration.Integration.condition
    run_request = integration.Integration.run_request
    task_create = integration.Integration.task_create
    extraction = integration.Integration.extraction
    read = integration.Integration.read

    def store(self):
        return Store(self.root, lambda path: Path(path))

    def sample_receipt(self, request_id, phase='settled', large=False):
        store = self.store()
        value = {'receipt': {'request_id': request_id, 'scope_id': store.scope, 'phase': phase},
                 'request': {'body': 'anonymous material\n' * (10000 if large else 1)},
                 'plans': [{'content': 'original'}]}
        store.save(value)
        return value

    def test_pending_cold_hot_and_complete_reads(self):
        expected = [self.sample_receipt('plain'), self.sample_receipt('compressed', large=True)]
        pending = self.sample_receipt('pending', 'prepared')
        store = self.store()
        paths = [filesystem_path(store.path(v['receipt']['request_id'])) for v in expected + [pending]]
        before = {p: p.read_bytes() for p in paths}
        with patch.object(storage, 'decode_receipt', wraps=storage.decode_receipt) as decode:
            self.assertEqual(store.pending(), [pending])
            self.assertEqual(decode.call_count, 3)
            self.assertEqual(self.store().pending(), [pending])
            self.assertEqual(decode.call_count, 4)
            self.assertEqual(store.pending(except_id='pending'), [])
            self.assertEqual(decode.call_count, 5)
            self.assertEqual(store.load('compressed'), expected[1])
            self.assertCountEqual(store.all(), expected + [pending])
            self.assertEqual(decode.call_count, 9)
        self.assertEqual({p: p.read_bytes() for p in paths}, before)
        self.assertFalse((store.state / 'lock').exists())

    def test_pending_rechecks_same_size_same_mtime_bytes(self):
        original = self.sample_receipt('mutable')
        store = self.store()
        path = filesystem_path(store.path('mutable'))
        self.assertEqual(store.pending(), [])
        before = path.stat()
        altered = copy.deepcopy(original)
        altered['receipt']['phase'] = 'waiting'
        raw = receipt_bytes(altered)
        self.assertEqual(len(raw), len(path.read_bytes()))
        path.write_bytes(raw)
        os.utime(path, ns=(before.st_atime_ns, before.st_mtime_ns))
        with patch.object(storage, 'decode_receipt', wraps=storage.decode_receipt) as decode:
            self.assertEqual(store.pending(), [altered])
            self.assertEqual(decode.call_count, 1)
        self.assertEqual(path.stat().st_mtime_ns, before.st_mtime_ns)

    def test_pending_cache_never_hides_corruption_or_foreign_identity(self):
        value = self.sample_receipt('checked', large=True)
        store = self.store()
        path = filesystem_path(store.path('checked'))
        original = path.read_bytes()
        envelope = json.loads(original)
        foreign = copy.deepcopy(value)
        foreign['receipt']['scope_id'] = 'local:foreign'
        wrong_id = copy.deepcopy(value)
        wrong_id['receipt']['request_id'] = 'wrong'
        broken_json = b'{broken'
        cases = [(b'{broken', 'indeterminate'),
                 (receipt_bytes(dict(envelope, payload=base64.b64encode(b'broken gzip').decode())), 'indeterminate'),
                 (receipt_bytes(dict(envelope,
                     payload=base64.b64encode(gzip.compress(broken_json, mtime=0)).decode(),
                     sha256=hashlib.sha256(broken_json).hexdigest(),
                     uncompressed_bytes=len(broken_json))), 'indeterminate'),
                 (receipt_bytes(foreign), 'invalid_scope'), (receipt_bytes(wrong_id), 'indeterminate')]
        for raw, code in cases:
            path.write_bytes(original)
            self.assertEqual(store.pending(), [])
            path.write_bytes(raw)
            with self.assertRaises(WorkflowError) as caught:
                store.pending()
            self.assertEqual(caught.exception.code, code)
            self.assertEqual(path.read_bytes(), raw)
        path.write_bytes(original)
        self.assertEqual(store.pending(), [])
        renamed = path.with_name('wrong-name.json')
        path.rename(renamed)
        with self.assertRaises(WorkflowError) as caught:
            store.pending()
        self.assertEqual(caught.exception.code, 'indeterminate')
        self.assertEqual(renamed.read_bytes(), original)

    def test_pending_discovers_new_receipts_and_isolates_mutable_results(self):
        self.sample_receipt('history')
        store = self.store()
        self.assertEqual(store.pending(), [])
        expected = self.sample_receipt('new', 'applying')
        result = store.pending()
        self.assertEqual(result, [expected])
        result[0]['receipt']['phase'] = 'settled'
        result[0]['plans'][0]['content'] = 'changed by caller'
        self.assertEqual(store.pending(), [expected])
        history = store.load('history')
        history['receipt']['scope_id'] = 'changed by caller'
        self.assertEqual(store.pending(), [expected])

    def test_pending_metadata_cache_is_bounded(self):
        with patch.object(storage, '_settled_receipts', storage.OrderedDict()), \
                patch.object(storage, 'SETTLED_RECEIPT_CACHE_LIMIT', 3):
            for index in range(7):
                self.sample_receipt(f'bounded-{index}', large=True)
            self.assertEqual(self.store().pending(), [])
            self.assertEqual(len(storage._settled_receipts), 3)
            for entry in storage._settled_receipts.values():
                self.assertEqual(len(entry), 4)
                self.assertIsInstance(entry[0], bytes)
                self.assertTrue(all(isinstance(item, str) for item in entry[1:]))

    def test_pending_large_history_reuses_cache_across_store_instances(self):
        store = self.store()
        filesystem_path(store.state / 'operations').mkdir(parents=True)
        for index in range(1181):
            request_id = f'history-{index}'
            value = {'receipt': {'request_id': request_id, 'scope_id': store.scope, 'phase': 'settled'},
                     'request': {'body': 'anonymous historical material'}}
            filesystem_path(store.path(request_id)).write_bytes(receipt_bytes(value))
        with patch.object(storage, '_settled_receipts', storage.OrderedDict()), \
                patch.object(storage, 'decode_receipt', wraps=storage.decode_receipt) as decode:
            self.assertEqual(self.store().pending(), [])
            self.assertEqual(decode.call_count, 1181)
            for _ in range(2):
                self.assertEqual(self.store().pending(), [])
                self.assertEqual(decode.call_count, 1181)
            self.assertEqual(len(storage._settled_receipts), 1181)

    def large_request(self):
        request = self.task_create()
        request['payload']['body'] = 'Anonymous repeated material 中文.\n' * 5000
        return request

    def test_large_settled_roundtrip_replay_and_allocation(self):
        request = self.large_request()
        response = self.run_request(request)
        store = self.store()
        value = store.load(request['request_id'])
        path = filesystem_path(store.path(request['request_id']))
        stored = path.read_bytes()
        self.assertIn('storage_format', json.loads(stored))
        self.assertLess(len(stored), len(receipt_bytes(value)) // 10)
        self.assertEqual(store.all(), [value])
        store.save(value)
        self.assertEqual(path.read_bytes(), stored)
        replay = self.run_request(request)
        self.assertTrue(replay.pop('replayed'))
        self.assertEqual(replay, response)
        next_response = self.run_request(self.task_create())
        self.assertNotEqual(next_response['receipt']['allocations'], response['receipt']['allocations'])
        print(f'Anonymous receipt: {len(receipt_bytes(value))} -> {len(stored)} bytes')

    def test_unsettled_receipts_remain_plain_and_resume(self):
        for stage in ('prepared', 'before_write:0'):
            with self.subTest(stage=stage):
                request = self.large_request()
                def crash(current, value):
                    if current == stage:
                        raise RuntimeError('simulated process interruption')
                with self.assertRaises(RuntimeError):
                    Workflow(self.root, fault=crash).execute(request)
                store = self.store()
                raw = filesystem_path(store.path(request['request_id'])).read_bytes()
                value = json.loads(raw)
                self.assertNotIn('storage_format', value)
                self.assertEqual(value['receipt']['phase'], 'prepared' if stage == 'prepared' else 'applying')
                self.assertEqual(value['request'], request)
                self.assertTrue(value['plans'][0]['content'])
                recovered = self.run_request(request)
                self.assertEqual(recovered['receipt']['allocations'], value['receipt']['allocations'])
                self.assertIn('storage_format', json.loads(filesystem_path(store.path(request['request_id'])).read_bytes()))

    def test_legacy_read_does_not_rewrite(self):
        request = self.large_request()
        self.run_request(request)
        store = self.store()
        value = store.load(request['request_id'])
        path = filesystem_path(store.path(request['request_id']))
        legacy = json.dumps(value, ensure_ascii=True, separators=(',', ':')).encode()
        path.write_bytes(legacy)
        self.assertEqual(store.load(request['request_id']), value)
        self.assertEqual(store.all(), [value])
        self.assertEqual(path.read_bytes(), legacy)

    def test_complete_value_survives_compression(self):
        store = self.store()
        value = store.prepare({'request_id': 'complete', 'operation': 'record.extract',
                               'payload': {'body': 'Original 中文\n' * 10000}},
                              'digest', [{'content': 'original plan', 'path': 'anonymous', 'before': None}],
                              [{'ref': {'id': 'T-001'}}], {'anonymous': 'revision'},
                              {'result': ['all', 'original', 'data']})
        value['receipt'].update(phase='settled', outcome='partial', recovery_actions=[{'action': 'resolve_conflict'}])
        value['errors'] = [{'code': 'revision_conflict', 'message': 'Original error'}]
        value['extension'] = {'future': 'Preserve unknown fields'}
        expected = copy.deepcopy(value)
        store.save(value)
        self.assertEqual(store.load('complete'), expected)
        self.assertEqual(store.all(), [expected])

    def test_small_settled_stays_plain(self):
        request = self.task_create()
        self.run_request(request)
        self.assertNotIn('storage_format', json.loads(filesystem_path(self.store().path(request['request_id'])).read_bytes()))

    def test_settled_partial_extraction_recovery(self):
        source = self.root / 'game-workflow/tasks/T-001-copy.md'
        source.write_text(source.read_text(encoding='utf-8').replace('<!-- workflow:endrecord EV-001 -->',
            'Anonymous evidence.\n' * 5000 + '<!-- workflow:endrecord EV-001 -->'), encoding='utf-8')
        request = self.extraction()
        def stop(stage, value):
            if stage == 'after_write:0':
                raise OSError('pause extraction')
        self.run_request(request, 'partial', Workflow(self.root, fault=stop))
        source.write_bytes(source.read_bytes() + b'\nUser context.\n')
        self.run_request(request, 'partial')
        store = self.store()
        path = filesystem_path(store.path(request['request_id']))
        self.assertIn('storage_format', json.loads(path.read_bytes()))
        self.assertEqual(store.load(request['request_id'])['receipt']['phase'], 'settled')
        destination = self.root / 'game-workflow/evidence/EV-001.md'
        before = destination.read_bytes()
        repair = self.request('record.extract', {'target': {'path': 'tasks/T-001-copy.md', 'fragment': 'EV-001'},
            'destination': 'evidence/EV-001.md', 'recovery_of': request['request_id']},
            [self.condition('tasks/T-001-copy.md'), self.condition('evidence/EV-001.md')])
        self.run_request(repair)
        self.assertEqual(destination.read_bytes(), before)
        self.assertIn(b'User context.', source.read_bytes())

    def test_corruption_scope_and_identity_fail_closed(self):
        request = self.large_request()
        self.run_request(request)
        store = self.store()
        path = filesystem_path(store.path(request['request_id']))
        original = path.read_bytes()
        envelope = json.loads(original)
        decoded = store.load(request['request_id'])
        cases = []
        for key, value in [('storage_format', 'unknown'), ('payload', 'invalid!'),
                           ('sha256', '0' * 64), ('uncompressed_bytes', 0),
                           ('payload', base64.b64encode(b'broken gzip').decode())]:
            altered = dict(envelope)
            altered[key] = value
            cases.append((altered, 'indeterminate'))
        for key, value, code in [('scope_id', 'local:foreign', 'invalid_scope'),
                                 ('request_id', 'foreign', 'indeterminate'),
                                 ('phase', 'applying', 'indeterminate')]:
            altered = copy.deepcopy(decoded)
            altered['receipt'][key] = value
            raw = receipt_bytes(altered)
            cases.append((dict(envelope, payload=base64.b64encode(gzip.compress(raw, mtime=0)).decode(),
                               sha256=hashlib.sha256(raw).hexdigest(), uncompressed_bytes=len(raw)), code))
        for altered, code in cases:
            with self.subTest(case=code, fields=altered.keys()):
                damaged = receipt_bytes(altered)
                path.write_bytes(damaged)
                for read in (lambda: store.load(request['request_id']), store.all, store.pending):
                    with self.assertRaises(WorkflowError) as caught:
                        read()
                    self.assertEqual(caught.exception.code, code)
                self.assertEqual(path.read_bytes(), damaged)
        path.write_bytes(original)

    def test_long_operation_path(self):
        self.root = self.folder / ('nested-' + 'a' * 90) / ('nested-' + 'b' * 90) / 'project'
        filesystem_path(self.root).mkdir(parents=True)
        store = self.store()
        value = {'receipt': {'request_id': 'long', 'scope_id': store.scope, 'phase': 'settled'},
                 'request': {'body': 'anonymous\n' * 10000}}
        with store.lock(write=True):
            store.save(value)
            self.assertEqual(store.load('long'), value)
            self.assertEqual(store.all(), [value])
        self.assertGreater(len(str(store.path('long'))), 260)

    def test_malformed_identity_and_shape_fail_closed(self):
        request = self.large_request()
        self.run_request(request)
        store = self.store()
        path = filesystem_path(store.path(request['request_id']))
        original = store.load(request['request_id'])
        malformed = []
        for key, bad in [('request_id', 123), ('scope_id', 123)]:
            value = copy.deepcopy(original)
            value['receipt'][key] = bad
            malformed.append(value)
        malformed.extend([[], {'receipt': []}, {'receipt': None}])
        for compressed in (False, True):
            for value in malformed:
                with self.subTest(compressed=compressed, value_type=type(value).__name__):
                    raw = receipt_bytes(value)
                    damaged = receipt_bytes({'storage_format': 'gamecaden.operation.gzip-base64.v1',
                        'uncompressed_bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                        'payload': base64.b64encode(gzip.compress(raw, mtime=0)).decode()}) if compressed else raw
                    path.write_bytes(damaged)
                    for read in (lambda: store.load(request['request_id']), store.all, store.pending):
                        with self.assertRaises(WorkflowError) as caught:
                            read()
                        self.assertEqual(caught.exception.code, 'indeterminate')
                    # A new creation reaches the all()/allocation scan; status reaches load().
                    for operation in (self.task_create(), self.request('operation.status', {'request_id': request['request_id']})):
                        result = self.run_request(operation, 'indeterminate')
                        self.assertEqual(result['errors'][0]['code'], 'indeterminate')
                    self.assertEqual(path.read_bytes(), damaged)


if __name__ == '__main__':
    unittest.main()
