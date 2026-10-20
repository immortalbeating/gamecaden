"""Lossless settled-receipt storage checks using disposable projects."""
import base64
import copy
import gzip
import hashlib
import json
from pathlib import Path
import unittest

import test_workflow_io as integration
from workflow_formats import WorkflowError
from workflow_io import Workflow
from workflow_storage import Store, filesystem_path, receipt_bytes


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
                for read in (lambda: store.load(request['request_id']), store.all):
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
                    for read in (lambda: store.load(request['request_id']), store.all):
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
