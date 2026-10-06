"""Navigation projection tests in disposable registered fixtures."""
import json, shutil, tempfile, unittest
from pathlib import Path
from test_workflow_governance import BUNDLE, RUN, make_case, block
from workflow_panel_data import PanelData
from workflow_governance import Governance
from workflow_navigation import headings

class NavigationTests(unittest.TestCase):
    def setUp(self):
        RUN.mkdir(parents=True,exist_ok=True)
        self.folder=Path(tempfile.mkdtemp(prefix='navigation-',dir=RUN)); self.root=self.folder/'project'
        make_case(self.root)
        self.addCleanup(shutil.rmtree,self.folder)
        self.child=self.root/'game-workflow/spec/combat.md'
        self.parent=self.root/'game-workflow/roadmap.md'
    def view(self): return Governance(PanelData(self.root)).build()
    def annotate(self,path,nav):
        # Amend existing standalone annotation, preserving all governing entries.
        from workflow_governance import BLOCK
        body=path.read_text(encoding='utf-8'); match=BLOCK.search(body)
        if match:
            model=json.loads(match[1]); model['navigation']=nav
            body=body[:match.start()]+block(model).strip()+body[match.end():]
        else: body+=block({'schema_version':1,'navigation':nav})
        path.write_text(body,encoding='utf-8')
    def node(self,view,path): return next(n for n in view['nodes'] if n.get('path')==str(path) and n.get('record_key'))
    def test_domain_parent_is_read_only_and_isolated_document_survives(self):
        task=self.root/'game-workflow/tasks/T-004-map.md'
        from workflow_governance import BLOCK
        body=task.read_text(encoding='utf-8');match=BLOCK.search(body);model=json.loads(match[1])
        model['flows']=[{'id':'navigation-invariance','title':'推进','scope':'test','authority':'effective','steps':[{'id':'produce','title':'制作','target':{'id':'T-004'},'action':'正式地图生产'}]}]
        task.write_text(body[:match.start()]+block(model)+body[match.end():],encoding='utf-8')
        before=self.view()
        self.assertTrue(before['flows'])
        self.annotate(self.child,{'domain':'combat','responsibility':'规范阅读','parent':{'path':'../roadmap.md'}})
        after=self.view(); node=self.node(after,self.child)
        self.assertEqual(node['navigation_domain'],'combat')
        self.assertEqual(node['navigation_parent_key'],self.node(after,self.parent)['key'])
        self.assertEqual(node['navigation_source_key'],node['key'])
        self.assertIsNone(self.node(after,self.parent)['navigation_domain'])
        for field in ('edges','conditions','flows','relationships','materials'):
            # Source revisions in condition proofs can change only with source content.
            self.assertEqual(before[field],after[field],field)
    def test_cycle_bad_and_non_document_parent(self):
        self.annotate(self.child,{'parent':{'path':'../roadmap.md'}})
        self.annotate(self.parent,{'parent':{'path':'spec/combat.md'}})
        v=self.view()
        self.assertEqual(sum(d['code']=='navigation_cycle' for d in v['diagnostics']),2)
        self.assertIsNone(self.node(v,self.child)['navigation_parent_key'])
        for ref in ({'path':'missing.md'},{'id':'T-004'},{'path':'combat.md'}):
            self.annotate(self.child,{'parent':ref});v=self.view()
            self.assertIsNone(self.node(v,self.child)['navigation_parent_key'])
            self.assertTrue(any(d['code'] in ('invalid_navigation_parent','invalid_navigation') for d in v['diagnostics']))
    def test_qualified_parent_and_unregistered_parent_fail(self):
        (self.root/'fixtures/unread.md').write_text('# unread',encoding='utf-8')
        for ref in ({'path':'../roadmap.md','source':'tasks'},
                    {'path':'../roadmap.md','project_id':'wrong-project'},
                    {'path':'../roadmap.md','id':'T-004'},
                    {'path':'../../fixtures/unread.md'}):
            self.annotate(self.child,{'parent':ref});v=self.view()
            self.assertIsNone(self.node(v,self.child)['navigation_parent_key'])
            self.assertTrue(any(d['code'] in ('invalid_navigation_parent','invalid_navigation') for d in v['diagnostics']))
    def test_fences_and_embedded_examples_are_not_headings(self):
        body='# Real\n```markdown\n## Example\n```\n~~~~\n# Example2\n~~~~\n<!-- workflow:record evidence EV-1 -->\n# Embedded\n<!-- workflow:endrecord EV-1 -->\n## End ###\n'
        self.assertEqual(headings(body),[{'text':'Real','level':1,'fragment':'Real'},{'text':'End','level':2,'fragment':'End'}])
        self.child.write_text(self.child.read_text(encoding='utf-8')+'\n```markdown\n## False Heading\n```\n## Actual Heading\n',encoding='utf-8')
        hs=self.node(self.view(),self.child)['headings']
        self.assertIn('Actual Heading',[h['text'] for h in hs]);self.assertNotIn('False Heading',[h['text'] for h in hs])
    def test_embedded_headings_and_navigation_keep_actual_owner(self):
        from workflow_formats import yaml_dump
        guard=PanelData(self.root)._project()
        record=guard.resolve({'id':'EV-001'})
        meta=dict(record.metadata);meta['id']='EV-990'
        text='\n<!-- workflow:record evidence EV-990 -->\n```yaml\n'+yaml_dump(meta)+'```\n# Embedded Heading\n'+block({'schema_version':1,'navigation':{'domain':'evidence'}})+'\n<!-- workflow:endrecord EV-990 -->\n'
        self.child.write_text(self.child.read_text(encoding='utf-8')+text,encoding='utf-8')
        view=self.view();outer=self.node(view,self.child)
        embedded=next(n for n in view['nodes'] if (n.get('ref') or {}).get('id')=='EV-990')
        self.assertNotIn('Embedded Heading',[h['text'] for h in outer['headings']])
        self.assertEqual(embedded['headings'],[{'text':'Embedded Heading','level':1,'fragment':'Embedded Heading'}])
        self.assertEqual(embedded['navigation_domain'],'evidence')
        self.assertIsNone(outer['navigation_domain'])
    def test_registered_raw_source_navigation(self):
        path=self.root/'fixtures/raw-notes.md'
        path.write_text('# Notes\n```markdown\n## Example\n```\n'+block({'schema_version':1,'navigation':{'domain':'design'}}),encoding='utf-8')
        panel=PanelData(self.root,external_sources=[{'id':'notes','label':'Notes','role':'spec','path':'fixtures/raw-notes.md'}])
        view=Governance(panel).build();node=self.node(view,path)
        self.assertEqual(node['navigation_domain'],'design')
        self.assertEqual(node['headings'],[{'text':'Notes','level':1,'fragment':'Notes'}])
        self.assertFalse(view['edges'])

    def test_invalid_navigation_does_not_change_conditions(self):
        before=self.view(); self.annotate(self.child,{'unexpected':'x'});after=self.view()
        self.assertEqual(before['conditions'],after['conditions'])
        self.assertEqual(before['edges'],after['edges'])
        self.assertTrue(any(d['code']=='invalid_navigation' for d in after['diagnostics']))

if __name__=='__main__': unittest.main()
