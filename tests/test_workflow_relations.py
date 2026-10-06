"""Isolated relation projection tests using existing governance fixtures."""
import copy
import itertools
import json
import re
import unittest
import test_workflow_governance as fixtures
block = fixtures.block
from workflow_relations import combine
from workflow_formats import revision


class RelationsTests(fixtures.GovernanceTests):
    def model(self):
        self.path = self.root / 'game-workflow/tasks/T-004-map.md'
        body = self.path.read_text(encoding='utf-8')
        self.prefix = body[:body.index('<!-- workflow:governance -->')]
        return json.loads(re.search(r'```json\s*\n(.*?)\n```', body, re.S)[1])

    def save(self, model):
        self.path.write_text(self.prefix + block(model), encoding='utf-8')

    def flow(self, requires=None, **changes):
        model = self.model()
        step = {'id':'produce','title':'正式制作','target':{'id':'T-004'},'action':'正式地图生产'}
        if requires is not None:
            step['requires'] = requires
        step.update(changes)
        model['flows'] = [{'id':'map-flow','title':'地图推进','scope':'关卡 A','authority':'effective','steps':[step]}]
        self.save(model)
        return model

    def test_original_has_empty_extensions(self):
        view = self.view()
        self.assertEqual(view['flows'], [])
        self.assertEqual(view['relationships'], [])

    def test_flow_only_is_structured(self):
        model=self.flow()
        for group in ('conditions','materials'):
            model.pop(group,None)
        self.save(model)
        for relative in ('game-workflow/roadmap.md','game-workflow/spec/combat.md'):
            path=self.root/relative
            path.write_text(re.sub(r'<!-- workflow:governance -->.*?<!-- workflow:endgovernance -->','',path.read_text(encoding='utf-8'),flags=re.S),encoding='utf-8')
        view=self.view()
        self.assertTrue(view['coverage']['structured'])
        self.assertFalse(any(d['code']=='governance_unmapped' for d in view['diagnostics']))
        self.assertEqual(view['flows'][0]['steps'][0]['status'],'unknown')

    def embedded(self, kind, model, identity):
        from workflow_formats import yaml_dump
        from workflow_panel_data import PanelData
        guard=PanelData(self.root)._project()
        original=guard.resolve({'id':'EV-001' if kind=='evidence' else 'D-001'})
        metadata=copy.deepcopy(original.metadata);metadata['id']=identity
        text='\n<!-- workflow:record '+kind+' '+identity+' -->\n```yaml\n'+yaml_dump(metadata)+'```\n'+block(model)+'\n<!-- workflow:endrecord '+identity+' -->\n'
        self.path.write_text(self.path.read_text(encoding='utf-8')+text,encoding='utf-8')

    def reversed_view(self):
        from workflow_panel_data import PanelData
        from workflow_governance import Governance
        panel=PanelData(self.root);snapshot=panel.snapshot
        def reversed_snapshot(**kwargs):
            page=snapshot(**kwargs);page['records']=list(reversed(page['records']));return page
        panel.snapshot=reversed_snapshot
        return Governance(panel).build()

    def test_embedded_flow_and_relationship_have_single_actual_owner(self):
        model=self.flow();definition=copy.deepcopy(model['flows'][0]);definition['id']='embedded-flow'
        self.embedded('evidence',{'schema_version':1,'flows':[definition]},'EV-900')
        relation={'id':'embedded-policy','from':{'id':'T-004'},'to':{'id':'T-002'},'kind':'provides_policy','authority':'effective'}
        self.embedded('decision',{'schema_version':1,'relationships':[relation]},'D-900')
        # A fenced governance example and a marker in ordinary text stay inactive.
        self.path.write_text(self.path.read_text(encoding='utf-8')+'\n~~~~text\n'+block({'schema_version':1,'flows':[definition]})+'\n~~~~\nordinary <!-- workflow:governance --> string\n',encoding='utf-8')
        for view in (self.view(),self.reversed_view()):
            self.assertFalse(any(d['code']=='invalid_governance' for d in view['diagnostics']))
            flows=view['flows'];self.assertEqual(len(flows),2)
            nodes={node['key']:node for node in view['nodes']}
            embedded=next(flow for flow in flows if flow['id']=='embedded-flow')
            self.assertEqual(nodes[embedded['source_key']]['ref']['id'],'EV-900')
            self.assertEqual(len(view['relationships']),1)
            self.assertEqual(nodes[view['relationships'][0]['source_key']]['ref']['id'],'D-900')
            self.assertEqual(len({step['key'] for flow in flows for step in flow['steps']}),2)

    def test_embedded_duplicate_flow_and_relationship_ids_fail_closed_in_either_order(self):
        model=self.flow();definition=copy.deepcopy(model['flows'][0])
        self.embedded('evidence',{'schema_version':1,'flows':[definition]},'EV-900')
        for view in (self.view(),self.reversed_view()):
            self.assertEqual(view['flows'],[])
            self.assertTrue(any(d['code']=='invalid_governance' for d in view['diagnostics']))
        model=self.flow();model['flows'][0]['id']='fresh-flow';self.save(model)
        relation={'id':'duplicate-policy','from':{'id':'T-004'},'to':{'id':'T-002'},'kind':'produces','authority':'effective'}
        self.embedded('evidence',{'schema_version':1,'relationships':[relation]},'EV-900')
        self.embedded('decision',{'schema_version':1,'relationships':[relation]},'D-900')
        for view in (self.view(),self.reversed_view()):
            self.assertEqual(view['flows'],[])
            self.assertEqual(view['relationships'],[])
            self.assertTrue(any(d['code']=='invalid_governance' for d in view['diagnostics']))

    def test_local_refs_keep_project_and_source_qualifiers(self):
        self.evidence()
        for qualifiers in ({'project_id':'foreign'}, {'source':'missing'}, {'source':'spec'}, {'project_id':'foreign','source':'missing'}):
            reference={'path':str(self.root/'game-workflow/tasks/T-004-map.md'),'fragment':'map-ready',**qualifiers}
            model=self.flow({'condition':reference})
            model['relationships']=[{'id':'bad-qualified','from':reference,'to':{'id':'T-002'},'kind':'defines','authority':'effective'}]
            self.save(model);view=self.view()
            self.assertEqual(view['flows'][0]['steps'][0]['status'],'unknown',qualifiers)
            self.assertEqual(view['relationships'],[],qualifiers)
            self.assertTrue(any(d['code']=='unresolved_relation' for d in view['diagnostics']))
        for reference in ({'path':str(self.path),'fragment':'map-ready','project_id':'example-game','source':'tasks'},
                          {'id':'T-004','fragment':'map-ready','project_id':'example-game','source':'tasks'}):
            self.flow({'condition':reference})
            self.assertEqual(self.view()['flows'][0]['steps'][0]['status'],'satisfied')

    def test_cross_cycle_with_satisfied_any_is_order_independent(self):
        self.evidence()
        reference={'condition':{'path':str(self.root/'game-workflow/tasks/T-004-map.md'),'fragment':'map-ready'}}
        model=self.flow()
        template=model['flows'][0]['steps'][0]
        definitions=[{**template,'id':'A','requires':{'all':[{'step':'B'},{'step':'C'}]}},
                     {**template,'id':'B','requires':{'step':'A'}},
                     {**template,'id':'C','requires':{'any':[{'step':'B'},reference]}}]
        independent={**template,'id':'independent','requires':reference}
        alternative={**template,'id':'alternative','requires':{'any':[{'step':'A'},reference]}}
        for order in itertools.permutations(definitions):
            model['flows'][0]['steps']=list(order)+[independent,alternative];self.save(model)
            steps={step['id']:step for step in self.view()['flows'][0]['steps']}
            for identity in ('A','B','C'):
                self.assertEqual(steps[identity]['status'],'unknown',[s['id'] for s in order])
                self.assertEqual(steps[identity]['requires']['state'],'unknown')
            self.assertEqual(steps['independent']['status'],'satisfied')
            self.assertEqual(steps['alternative']['status'],'satisfied')

    def test_condition_provenance_and_no_writes(self):
        self.evidence()
        self.flow({'condition':{'path':str(self.root/'game-workflow/tasks/T-004-map.md'),'fragment':'map-ready'}})
        before = {str(p):revision(p.read_bytes()) for p in self.root.rglob('*') if p.is_file()}
        view = self.view(); step = view['flows'][0]['steps'][0]
        self.assertEqual(step['status'],'satisfied')
        self.assertEqual(step['requires']['state'],'satisfied')
        self.assertEqual(step['condition_keys'], [view['conditions'][0]['key']])
        self.assertEqual(view['conditions'][0]['expected_check'], {'kind':'evidence','actor_kind':None})
        self.assertEqual(before, {str(p):revision(p.read_bytes()) for p in self.root.rglob('*') if p.is_file()})
        self.assertTrue(any(n['kind']=='step' and n['target_key']==step['target_key'] for n in view['nodes']))
        self.assertTrue(any(r['ref']['path']==str(self.path) for r in view['source_revisions']))

    def test_wrong_target_action_and_advisory(self):
        self.evidence()
        ref = {'condition':{'path':str(self.root/'game-workflow/tasks/T-004-map.md'),'fragment':'map-ready'}}
        for changes in ({'action':'候选交接'}, {'target':{'id':'T-002'}}, {'target':{'path':str(self.root/'fixtures/blueprint.md')}}):
            self.flow(ref, **changes)
            self.assertEqual(self.view()['flows'][0]['steps'][0]['status'],'unknown')
        for field,value in [('authority','proposed'),('authority','reference'),('strength','advisory')]:
            model = self.flow(ref); model['conditions'][0][field]=value; self.save(model)
            self.assertEqual(self.view()['flows'][0]['steps'][0]['status'],'unknown')
        model=self.flow(ref);model['flows'][0]['authority']='proposed';self.save(model)
        self.assertEqual(self.view()['flows'][0]['steps'][0]['status'],'unknown')

    def test_machine_pass_does_not_satisfy_user_decision(self):
        self.evidence()
        model=self.flow({'condition':{'path':str(self.root/'game-workflow/tasks/T-004-map.md'),'fragment':'map-ready'}})
        model['conditions'][0]['check'].update(kind='decision',actor_kind='user');self.save(model)
        view=self.view()
        self.assertEqual(view['conditions'][0]['expected_check'], {'kind':'decision','actor_kind':'user'})
        self.assertEqual(view['flows'][0]['steps'][0]['status'],'unknown')

    def test_unknown_missing_cycles_and_transitive_affected(self):
        model=self.flow({'step':'missing'})
        self.assertEqual(self.view()['flows'][0]['steps'][0]['status'],'unknown')
        step=model['flows'][0]['steps'][0];step['requires']={'step':'second'}
        second=copy.deepcopy(step);second.update(id='second',requires={'step':'produce'})
        third=copy.deepcopy(step);third.update(id='third',requires={'step':'second'})
        model['flows'][0]['steps'] += [second,third];self.save(model)
        view=self.view();steps=view['flows'][0]['steps']
        self.assertTrue(all(s['status']=='unknown' for s in steps))
        self.assertEqual(set(steps[0]['affected_keys']),{steps[1]['key'],steps[2]['key']})
        self.assertTrue(any(d['code']=='cyclic_steps' for d in view['diagnostics']))
        self.flow();self.assertEqual(self.view()['flows'][0]['steps'][0]['status'],'unknown')

    def test_failed_stale_and_explicit_na(self):
        ref={'condition':{'path':str(self.root/'game-workflow/tasks/T-004-map.md'),'fragment':'map-ready'}}
        self.evidence('failed');self.flow(ref)
        self.assertEqual(self.view()['flows'][0]['steps'][0]['status'],'unsatisfied')
        (self.root/'fixtures/blueprint.md').write_text('changed',encoding='utf-8')
        self.assertEqual(self.view()['flows'][0]['steps'][0]['status'],'stale')
        model=self.model();model['conditions'][0].update(applicability='not_applicable',applicability_reason='无此范围');self.save(model)
        self.assertEqual(self.view()['flows'][0]['steps'][0]['status'],'not_applicable')

    def test_nested_combinations_keep_unknown_above_stale(self):
        self.evidence()
        ref={'condition':{'path':str(self.root/'game-workflow/tasks/T-004-map.md'),'fragment':'map-ready'}}
        missing={'step':'missing'}
        self.flow({'any':[ref,missing]})
        self.assertEqual(self.view()['flows'][0]['steps'][0]['status'],'satisfied')
        (self.root/'fixtures/blueprint.md').write_text('changed',encoding='utf-8')
        self.flow({'all':[ref,{'any':[missing]}]})
        step=self.view()['flows'][0]['steps'][0]
        self.assertEqual(step['status'],'unknown')
        self.assertEqual(step['requires']['all'][0]['state'],'stale')

    def test_revision_consistency_includes_definitions(self):
        from unittest.mock import patch
        from workflow_relations import build_relations
        from workflow_panel_data import PanelDataError
        self.flow()
        def changing(governance):
            result=build_relations(governance)
            self.path.write_text(self.path.read_text(encoding='utf-8')+'\nchanged',encoding='utf-8')
            return result
        with patch('workflow_relations.build_relations',side_effect=changing):
            with self.assertRaises(PanelDataError) as raised:
                self.view()
        self.assertEqual(raised.exception.code,'revision_conflict')

    def test_typed_direction_and_source(self):
        model=self.flow()
        model['relationships']=[{'id':'policy','from':{'id':'T-004'},'to':{'id':'T-002'},'kind':'provides_policy','authority':'effective','label':'策略来源'}]
        self.save(model);view=self.view();relation=view['relationships'][0]
        nodes={n['key']:n for n in view['nodes']}
        self.assertEqual(nodes[relation['from']]['ref']['id'],'T-004')
        self.assertEqual(nodes[relation['to']]['ref']['id'],'T-002')
        self.assertEqual(relation['source_key'],view['flows'][0]['source_key'])
        self.assertIn(relation,view['edges'])

    def test_invalid_expression_duplicate_step_and_local_ids(self):
        for mutate in (lambda m:m['flows'][0]['steps'][0].update(requires={'all':[]}),
                       lambda m:m['flows'][0]['steps'][0].update(requires={'all':[{'step':'produce'}],'any':[{'step':'produce'}]}),
                       lambda m:m['flows'][0]['steps'].append(copy.deepcopy(m['flows'][0]['steps'][0])),
                       lambda m:m['flows'][0].update(id='map-ready')):
            model=self.flow();mutate(model);self.save(model)
            view=self.view();self.assertEqual(view['flows'],[])
            self.assertTrue(any(d['code']=='invalid_governance' for d in view['diagnostics']))


class CombinationTests(unittest.TestCase):
    def test_all_any_state_matrix(self):
        states=('satisfied','unsatisfied','unknown','stale','not_applicable')
        for left,right in itertools.product(states,repeat=2):
            values=[v for v in (left,right) if v!='not_applicable']
            all_expected=('not_applicable' if not values else 'unsatisfied' if 'unsatisfied' in values else
                          'unknown' if 'unknown' in values else 'stale' if 'stale' in values else 'satisfied')
            any_expected=('not_applicable' if not values else 'satisfied' if 'satisfied' in values else
                          'unknown' if 'unknown' in values else 'stale' if 'stale' in values else 'unsatisfied')
            self.assertEqual(combine('all',[left,right]),all_expected,(left,right))
            self.assertEqual(combine('any',[left,right]),any_expected,(left,right))


if __name__=='__main__':
    unittest.main()
