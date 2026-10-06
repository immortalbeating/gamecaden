"""Read-only flow prerequisite and typed relationship projection."""
import hashlib
from pathlib import Path
from workflow_formats import canonical, WorkflowError
from workflow_panel_data import PanelDataError


def combine(kind, states):
    applicable = [state for state in states if state != 'not_applicable']
    if not applicable:
        return 'not_applicable'
    if kind == 'all':
        if 'unsatisfied' in applicable:
            return 'unsatisfied'
        if all(state == 'satisfied' for state in applicable):
            return 'satisfied'
    elif 'satisfied' in applicable:
        return 'satisfied'
    for state in ('unknown', 'stale'):
        if state in applicable:
            return state
    return 'unsatisfied'


def build_relations(gov):
    flows, relationships = [], []
    conditions = {c['key']: c for c in gov.conditions}
    extensions = [(model,row) for model,row in gov.extensions if row['path'] not in gov.invalid_paths]

    def key_for(path, local_id):
        return 'local:' + hashlib.sha256(canonical([path, local_id]).encode()).hexdigest()

    def resolve(ref, base, source):
        try:
            return gov.resolve(ref, base)
        except (WorkflowError, PanelDataError) as exc:
            gov.diagnostic('unresolved_relation', str(exc), source)
            return None

    # Register every flow before resolving references across definition sources.
    for model, row in extensions:
        for definition in model.get('flows', []):
            key = key_for(row['path'], definition['id'])
            gov.locals[(row['path'], definition['id'])] = key
            flow = {k: definition[k] for k in ('id', 'title', 'scope', 'authority')}
            flow.update(key=key, source_key='record:' + row['key'], record_key=row['key'], steps=[])
            gov.add({**flow, 'kind': 'flow', 'path': row['path'], 'revision': row['revision'],
                     'ref': {'path': row['path'], 'fragment': definition['id']}})
            gov.edge(key, flow['source_key'], 'defined_in')
            flows.append(flow)
            for step in definition['steps']:
                step_key = 'step:' + hashlib.sha256(canonical([row['path'], definition['id'], step['id']]).encode()).hexdigest()
                item = {k: step[k] for k in ('id', 'title', 'action')}
                item.update(key=step_key, group=step.get('group'), target_key=None,
                            status='unknown', reason='尚未定义前提', condition_keys=[],
                            predecessor_keys=[], affected_keys=[], requires=None)
                flow['steps'].append(item)
                gov.add({**item, 'kind': 'step', 'source_key': flow['source_key'],
                         'record_key': row['key'], 'path': row['path'], 'revision': row['revision']})
                gov.edge(key, step_key, 'contains')

    index = 0
    for model, row in extensions:
        base = Path(row['reference_base'])
        for definition in model.get('flows', []):
            flow = flows[index]; index += 1
            steps = {s['id']: s for s in flow['steps']}
            definitions = {s['id']: s for s in definition['steps']}
            for step in flow['steps']:
                step['target_key'] = resolve(definitions[step['id']]['target'], base, flow['source_key'])
                gov.edge(step['key'], step['target_key'], 'references')
            def step_refs(expr):
                if not expr:
                    return set()
                if 'step' in expr:
                    return {expr['step']}
                return set().union(*(step_refs(child) for kind in ('all','any') for child in expr.get(kind,[])))

            graph={identity:step_refs(value.get('requires')) & steps.keys() for identity,value in definitions.items()}
            cycles=set()
            for identity in graph:
                frontier=list(graph[identity]);seen=set()
                while frontier:
                    current=frontier.pop()
                    if current==identity:
                        cycles.add(identity);break
                    if current not in seen:
                        seen.add(current);frontier.extend(graph[current])
            visiting, done = [], set(cycles)
            for identity in cycles:
                steps[identity].update(status='unknown',reason='步骤前提存在循环')
                gov.diagnostic('cyclic_steps','流程步骤前提存在循环',steps[identity]['key'])

            def expression(expr, step):
                kind = next(iter(expr))
                value = expr[kind]
                result = {kind: value, 'key': None, 'state': 'unknown', 'reason': ''}
                if kind in ('all', 'any'):
                    children = [expression(child, step) for child in value]
                    result[kind] = children
                    result.update(state=combine(kind, [c['state'] for c in children]), reason='按声明组合当前适用前提')
                elif kind == 'condition':
                    key = resolve(value, base, flow['source_key']); result['key'] = key
                    condition = conditions.get(key)
                    if key in conditions:
                        step['condition_keys'].append(key)
                        gov.edge(step['key'], key, 'requires')
                    if condition is None:
                        result['reason'] = '引用未定位到当前条件'
                    elif condition['authority'] != 'effective' or condition['strength'] != 'required':
                        result['reason'] = '条件不是生效的必要约束'
                    elif step['target_key'] not in condition['applies_to'] or condition['action'] != step['action']:
                        result['reason'] = '条件对象或动作与本步骤不匹配'
                    else:
                        result.update(state=condition['state'], reason=condition['reason'])
                else:
                    predecessor = steps.get(value)
                    if predecessor is None:
                        result['reason'] = '同一流程中缺少引用步骤'
                        gov.diagnostic('unresolved_step', result['reason'] + ': ' + value, step['key'])
                    else:
                        result['key'] = predecessor['key']
                        step['predecessor_keys'].append(predecessor['key'])
                        gov.edge(step['key'], predecessor['key'], 'requires')
                        evaluate(value)
                        result.update(state=predecessor['status'], reason=predecessor['reason'])
                return result

            def evaluate(step_id):
                if step_id in done:
                    return
                if step_id in visiting:
                    cycles.update(visiting[visiting.index(step_id):])
                    gov.diagnostic('cyclic_steps', '流程步骤前提存在循环', steps[step_id]['key'])
                    return
                visiting.append(step_id)
                step = steps[step_id]
                expr = definitions[step_id].get('requires')
                if expr:
                    step['requires'] = expression(expr, step)
                    step.update(status=step['requires']['state'], reason=step['requires']['reason'])
                if step_id in cycles:
                    step.update(status='unknown', reason='步骤前提存在循环')
                if flow['authority'] != 'effective':
                    step.update(status='unknown', reason='流程尚非生效定义')
                target = gov.nodes.get(step['target_key'], {})
                if target.get('kind') not in ('task', 'epic', 'asset'):
                    step.update(status='unknown', reason='步骤没有匹配的真实作用对象')
                visiting.pop(); done.add(step_id)

            # Mark the whole cyclic component before evaluating any expression;
            # a satisfied OR branch cannot make a circular member ready.
            for step_id in cycles:
                expr=definitions[step_id].get('requires')
                if expr:
                    steps[step_id]['requires']=expression(expr,steps[step_id])
                    steps[step_id]['requires'].update(state='unknown',reason='步骤前提存在循环')
            for step_id in steps:
                evaluate(step_id)
            # Affected means transitive reference, never an automatic blocking action.
            for step in flow['steps']:
                frontier = {step['key']}; affected = set()
                while frontier:
                    found = {s['key'] for s in flow['steps'] if s['key'] != step['key'] and
                             frontier.intersection(s['predecessor_keys'])} - affected
                    affected.update(found); frontier = found
                step['affected_keys'] = sorted(affected)
                for field in ('condition_keys', 'predecessor_keys'):
                    step[field] = list(dict.fromkeys(step[field]))
                gov.nodes[step['key']].update(step)
        for definition in model.get('relationships', []):
            source = 'record:' + row['key']
            origin = resolve(definition['from'], base, source)
            target = resolve(definition['to'], base, source)
            if origin is None or target is None:
                continue
            item = {'from': origin, 'to': target, 'relation': definition['kind'],
                    'source_key': source, 'label': definition.get('label'), 'authority': definition['authority'],
                    'definition_id': definition['id'], 'definition_ref': {**row['ref'], 'fragment': definition['id']}, 'revision': row['revision']}
            relationships.append(item)
            gov.edges.append(dict(item))
    return flows, relationships
