"""Content-based revision checks over isolated source fixtures and HTTP boundaries."""
import os, shutil, subprocess, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from workflow_panel_data import PanelData
from workflow_project import Project
from workflow_storage import filesystem_path
from workflow_formats import yaml_load, yaml_dump, Document
import workflow_panel_revisions as probes
import test_workflow_panel_server as bridge

BUNDLE=(Path(__file__).resolve().parents[1] / "plugins" / "gamecaden")
RUN=BUNDLE.parents[1]/'work/panel-revisions-eval/tests'

class RevisionTests(unittest.TestCase):
    def setUp(self):
        RUN.mkdir(parents=True,exist_ok=True)
        self.folder=Path(tempfile.mkdtemp(prefix='revisions-',dir=RUN));self.addCleanup(self.cleanup_fixture)
        self.root=self.folder/'project';shutil.copytree(BUNDLE/'examples/v1/project',self.root)
        self.panel=PanelData(self.root)
    def cleanup_fixture(self):
        self.assertTrue(self.folder.resolve().is_relative_to(RUN.resolve()))
        shutil.rmtree(filesystem_path(self.folder))
    def long_file(self, base):
        folder=base
        while len(str(folder/'source.md'))<290:
            folder/='nested-source-segment'
        filesystem_path(folder).mkdir(parents=True,exist_ok=True)
        path=folder/'source.md'
        filesystem_path(path).write_bytes((self.root/'game-workflow/spec/combat.md').read_bytes())
        return path
    def assert_direct_revision(self, path):
        result=self.check()
        row=next(r for r in result['source_revisions'] if r['ref']['path']==str(path))
        direct=self.panel._call('record.read',{'target':{'path':str(path)}})
        self.assertEqual(row['revision'],direct['revision'])
        self.assertFalse(row['ref']['path'].startswith('\\\\?\\'))
        return result
    def test_long_file_source_matches_direct_read(self):
        path=self.long_file(self.root/'long-file')
        mapping=self.root/'game-workflow/workspace.yaml';model=yaml_load(mapping.read_text(encoding='utf-8'))
        source=next(s for s in model['sources'] if s['id']=='spec')
        source.update(kind='file',path=os.path.relpath(path,mapping.parent))
        mapping.write_text(yaml_dump(model),encoding='utf-8')
        self.assert_direct_revision(path)
        filesystem_path(path).unlink()
        bad=self.panel.revisions();self.assertFalse(bad['complete'])
        self.assertTrue(any(d['code']=='not_found' and d['ref']['path']==str(path) for d in bad['diagnostics']))
    def test_long_collection_matches_direct_read_and_excludes_reserved_folders(self):
        path=self.long_file(self.root/'game-workflow/spec')
        for name in ('.git','.game-workflow-io'):
            hidden=filesystem_path(path.parent/name);hidden.mkdir();(hidden/'hidden.md').write_text('# hidden',encoding='utf-8')
        result=self.assert_direct_revision(path)
        self.assertFalse(any(r['ref']['path'].endswith('hidden.md') for r in result['source_revisions']))
        stamp=filesystem_path(path).stat()
        filesystem_path(path).write_bytes(filesystem_path(path).read_bytes()+b'\nchanged')
        os.utime(filesystem_path(path),ns=(stamp.st_atime_ns,stamp.st_mtime_ns))
        self.assertNotEqual(result['digest'],self.check()['digest'])
    def test_collection_excludes_linked_directory_and_rejects_linked_file(self):
        outside=self.folder/'outside';outside.mkdir();(outside/'escape.md').write_text('# outside',encoding='utf-8')
        link=self.root/'game-workflow/spec/linked'
        try:link.symlink_to(outside,target_is_directory=True)
        except OSError as exc:self.skipTest('Symbolic links unavailable: '+str(exc))
        result=self.check();self.assertFalse(any('escape.md' in r['ref']['path'] for r in result['source_revisions']))
        file_link=self.root/'game-workflow/spec/escape.md';file_link.symlink_to(outside/'escape.md')
        bad=self.panel.revisions();self.assertFalse(bad['complete'])
        self.assertTrue(any(d['code']=='invalid_scope' for d in bad['diagnostics']))
    @unittest.skipUnless(os.name=='nt','Windows junction regression')
    def test_long_collection_excludes_junction(self):
        path=self.long_file(self.root/'game-workflow/spec')
        outside=self.folder/'outside';outside.mkdir();(outside/'escape.md').write_text('# outside',encoding='utf-8')
        link=path.parent/'linked'
        created=subprocess.run(['cmd','/c','mklink','/J',str(filesystem_path(link)),str(outside)],capture_output=True)
        self.assertEqual(created.returncode,0,created.stderr)
        try:
            result=self.assert_direct_revision(path)
            self.assertFalse(any('escape.md' in r['ref']['path'] for r in result['source_revisions']))
        finally:filesystem_path(link).rmdir()
    def test_sample_reuses_observed_hash_and_collection_read_failure_is_logical(self):
        with patch.object(probes,'revision',side_effect=AssertionError('duplicate hash')):
            material,diagnostics=probes._sample(self.panel)
        self.assertFalse(diagnostics);self.assertTrue(material['source_revisions'])
        path=self.long_file(self.root/'game-workflow/spec')
        original=probes.os.walk
        def walk(root,**kwargs):
            if Path(root)==filesystem_path(self.root/'game-workflow/spec'):
                kwargs['onerror'](PermissionError(13,'denied',str(filesystem_path(path.parent))))
                return iter(())
            return original(root,**kwargs)
        with patch.object(probes.os,'walk',side_effect=walk):bad=self.panel.revisions()
        self.assertFalse(bad['complete']);self.assertIsNone(bad['digest'])
        self.assertTrue(any(d['code']=='read_failed' and d['ref']['path']==str(path.parent) for d in bad['diagnostics']))
    def check(self):
        value=self.panel.revisions();self.assertTrue(value['complete'],value['diagnostics']);self.assertIsNotNone(value['digest']);return value
    def test_stable_and_no_record_or_governance_parsing(self):
        from workflow_governance import Governance
        with patch.object(Project,'scan',side_effect=AssertionError('must not scan records')),patch.object(Document,'__init__',side_effect=AssertionError('must not parse documents')),patch.object(Governance,'build',side_effect=AssertionError('must not derive governance')):
            first=self.check();second=self.check()
        self.assertEqual(first,second)
        self.assertFalse((self.root/'.game-workflow-io').exists())
    def test_uncreated_collection_is_an_observed_empty_location(self):
        mapping=self.root/'game-workflow/workspace.yaml';model=yaml_load(mapping.read_text(encoding='utf-8'))
        model['sources'].append({'id':'future','role':'notes','kind':'collection','path':'future','owner':'project','format':'native-markdown-v1'})
        mapping.write_text(yaml_dump(model),encoding='utf-8')
        absent=self.check()
        folder=self.root/'game-workflow/future';folder.mkdir();path=folder/'new.md';path.write_text('# New',encoding='utf-8')
        created=self.check();self.assertNotEqual(absent['digest'],created['digest'])
        path.unlink();folder.rmdir()
        self.assertEqual(absent['digest'],self.check()['digest'])
        folder.write_text('Wrong source type',encoding='utf-8')
        bad=self.panel.revisions();self.assertFalse(bad['complete']);self.assertIsNone(bad['digest'])
        self.assertTrue(any(row['code']=='invalid_scope' for row in bad['diagnostics']))
    def test_collection_add_modify_delete_and_same_mtime(self):
        initial=self.check()['digest'];path=self.root/'game-workflow/spec/new.md'
        path.write_text('# One',encoding='utf-8');added=self.check()['digest'];self.assertNotEqual(initial,added)
        stamp=path.stat();path.write_text('# Two',encoding='utf-8');os.utime(path,ns=(stamp.st_atime_ns,stamp.st_mtime_ns))
        modified=self.check()['digest'];self.assertNotEqual(added,modified)
        path.unlink();self.assertEqual(initial,self.check()['digest'])
    def test_external_file_mapping_binding_and_unregistered_files(self):
        self.panel=PanelData(self.root,project_id='old',external_sources=[{'id':'vision','label':'Vision','role':'vision','path':'game-workflow/vision.md'}])
        first=self.check()['digest'];p=self.root/'game-workflow/vision.md';p.write_bytes(p.read_bytes()+b'\n');second=self.check()['digest'];self.assertNotEqual(first,second)
        (self.root/'unregistered.md').write_text('# Invisible',encoding='utf-8');self.assertEqual(second,self.check()['digest'])
        mapping=self.root/'game-workflow/workspace.yaml';mapping.write_bytes(mapping.read_bytes()+b'\n# changed mapping\n');third=self.check()['digest'];self.assertNotEqual(second,third)
        self.panel.project_id='other';self.assertNotEqual(third,self.check()['digest'])
        p.unlink();bad=self.panel.revisions();self.assertFalse(bad['complete']);self.assertIsNone(bad['digest']);self.assertTrue(any(d['code']=='not_found' for d in bad['diagnostics']))
    def test_mapping_new_collection_and_missing_source(self):
        first=self.check()['digest'];p=self.root/'game-workflow/workspace.yaml';model=yaml_load(p.read_text(encoding='utf-8'))
        folder=self.root/'game-workflow/more';folder.mkdir();(folder/'new.md').write_text('# new',encoding='utf-8')
        self.assertEqual(first,self.check()['digest'])
        model['sources'].append({'id':'more','role':'notes','kind':'collection','path':'more','owner':'project','format':'native-markdown-v1'});p.write_text(yaml_dump(model),encoding='utf-8')
        next_view=self.check();self.assertNotEqual(first,next_view['digest']);self.assertTrue(any(r['ref']['path'].endswith('new.md') for r in next_view['source_revisions']))
        shutil.rmtree(folder);removed=self.check();self.assertNotEqual(next_view['digest'],removed['digest'])
        self.assertFalse(any(row['ref']['path'].endswith('new.md') for row in removed['source_revisions']))
    def test_observed_read_race_never_reports_unchanged(self):
        original=probes._sample;calls=0
        def sample(panel):
            nonlocal calls
            result=original(panel);calls+=1
            if calls==1:
                p=self.root/'game-workflow/vision.md';p.write_bytes(p.read_bytes()+b'\nchanged')
            return result
        with patch.object(probes,'_sample',side_effect=sample):bad=self.panel.revisions()
        self.assertFalse(bad['complete']);self.assertIsNone(bad['digest']);self.assertTrue(any(d['code']=='revision_conflict' for d in bad['diagnostics']))
    def test_linked_source_and_out_of_root_are_not_read(self):
        self.panel=PanelData(self.root,external_sources=[{'id':'escape','label':'Escape','role':'notes','path':'../outside.md'}])
        (self.folder/'outside.md').write_text('outside',encoding='utf-8');bad=self.panel.revisions()
        self.assertFalse(bad['complete']);self.assertIsNone(bad['digest']);self.assertEqual(bad['source_revisions'],[])

class RevisionHttpTests(unittest.TestCase):
    def setUp(self):
        self.host=bridge.BridgeTests('test_session_origin_csrf_and_endpoint_bounds');self.host.setUp();self.addCleanup(self.host.stop)
    def test_revisions_authenticated_native_external_and_no_scope_parameter(self):
        h=self.host
        self.assertEqual(h.request('GET','/api/projects/lab/revisions',cookie=False)[0],401)
        self.assertEqual(h.request('GET','/api/projects/lab/revisions',headers={'Origin':'https://evil.example'})[0],403)
        self.assertEqual(h.request('GET','/api/projects/lab/revisions',headers={'Host':'evil.example'})[0],403)
        self.assertEqual(h.request('GET','/api/projects/lab/revisions?path=../outside.md')[0],400)
        self.assertEqual(h.request('GET','/api/projects/unknown/revisions')[0],404)
        with patch.object(Project,'scan',side_effect=AssertionError('must not scan records')),patch.object(Document,'__init__',side_effect=AssertionError('must not parse documents')):
            value=h.get('revisions');self.assertTrue(value['complete'],value)
            status,_,raw=h.request('GET','/api/projects/old/revisions');self.assertEqual(status,200);self.assertTrue(raw['complete'],raw)
        self.assertNotEqual(value['digest'],raw['digest'])
        self.assertEqual(len(raw['source_revisions']),1)

if __name__=='__main__':unittest.main()
