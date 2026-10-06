"""Read-only document navigation; never contributes governance edges or state."""
import re
from pathlib import Path
from workflow_formats import WorkflowError, json_load
from workflow_panel_data import PanelDataError


def headings(body):
    result=[]; fence=None; embedded=None; governance=False
    for line in body.splitlines():
        stripped=line.strip()
        if fence:
            if re.fullmatch(re.escape(fence[0])+"{"+str(fence[1])+",}\\s*", stripped): fence=None
            continue
        opening=re.match(r"^ {0,3}(`{3,}|~{3,})",line)
        if opening:
            fence=(opening[1][0],len(opening[1])); continue
        if stripped.startswith("<!-- workflow:record "):
            embedded=True; continue
        if stripped.startswith("<!-- workflow:endrecord "):
            embedded=None; continue
        if stripped=="<!-- workflow:governance -->": governance=True; continue
        if stripped=="<!-- workflow:endgovernance -->": governance=False; continue
        if embedded or governance: continue
        match=re.match(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*$",line)
        if match:
            text=re.sub(r"[ \t]+#+[ \t]*$","",match[2])
            result.append({'text':text,'level':len(match[1]),'fragment':text})
    return result


def build_navigation(gov):
    from workflow_governance import annotation_blocks, VALIDATOR
    declarations={}; candidates={}
    # Snapshot records are the access boundary, including externally bound raw sources.
    rows={"record:"+r['key']:r for r in gov.rows}
    for key,node in list(gov.nodes.items()):
        if not key.startswith('record:') or 'record_key' not in node: continue
        node.update(navigation_domain=None,navigation_responsibility=None,
                    navigation_parent_key=None,navigation_source_key=None,headings=[])
        try:
            body=gov.bodies.get(key)
            if body is None:
                row=rows.get(key)
                if row and row['interpretation']!='native':
                    body=gov.panel.read(row['key']).get('body') or ''
                else:
                    record=gov.guard.resolve(node['ref'])
                    body=record.body or ''
                    if record.span is None:
                        for start,end in sorted((r.span for r in gov.guard.documents[record.path].records if r.span is not None),reverse=True):
                            body=body[:start]+body[end:]
            node['headings']=headings(body)
            blocks=annotation_blocks(body)
            if len(blocks)>1: raise ValueError('每个来源记录最多一个治理块')
            if not blocks: continue
            model=json_load(blocks[0])
            if 'navigation' not in model: continue
            errors=list(VALIDATOR.iter_errors({'schema_version':1,'navigation':model['navigation']}))
            if errors: raise ValueError(errors[0].message)
            nav=model['navigation']; declarations[key]=nav
            node.update(navigation_domain=nav.get('domain'),navigation_responsibility=nav.get('responsibility'),navigation_source_key=key)
        except (WorkflowError,PanelDataError,ValueError,TypeError) as exc:
            gov.diagnostic('invalid_navigation',str(exc),key)
    for key,nav in declarations.items():
        if 'parent' not in nav: continue
        try:
            if gov.nodes[key]['kind']!='document': raise ValueError('文档父子归属仅适用于 document')
            row=rows.get(key); base=Path(row['reference_base'] or row['path']).parent if row and not row['reference_base'] else Path(row['reference_base']) if row else Path(gov.nodes[key]['path']).parent
            ref=nav['parent']
            if 'path' in ref:
                path=gov.guard.path(ref['path'],base)
                if not any(n.get('record_key') and n['path']==str(path) for n in gov.nodes.values()):
                    raise ValueError('父文档不在已读取来源中')
            record=gov.guard.resolve(ref,base)
            if ref.get('id') and record.id!=ref['id']: raise ValueError('Parent record ID does not match qualified path')
            matches=[n['key'] for n in gov.nodes.values() if n['key'].startswith('record:') and n.get('record_key') and n['path']==str(record.path) and (n.get('metadata') or {}).get('id')==record.id]
            if len(matches)!=1: raise ValueError('父文档不在已读取来源中或来源不唯一')
            parent=matches[0]
            if gov.nodes[parent]['kind']!='document': raise ValueError('父对象不是 document')
            if parent==key: raise ValueError('文档不能引用自身为父对象')
            candidates[key]=parent
        except (WorkflowError,PanelDataError,ValueError,TypeError) as exc:
            gov.diagnostic('invalid_navigation_parent',str(exc),key)
    cyclic=set()
    for start in candidates:
        chain=[]; current=start
        while current in candidates:
            if current in chain:
                cyclic.update(chain[chain.index(current):]); break
            chain.append(current); current=candidates[current]
    for key,parent in candidates.items():
        if key in cyclic: gov.diagnostic('navigation_cycle','文档父子归属存在循环',key)
        else: gov.nodes[key]['navigation_parent_key']=parent

