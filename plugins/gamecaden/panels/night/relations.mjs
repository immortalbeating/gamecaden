import {selectSources,diagramModel,computeLayout,flattenLayout,responsibility,displayTitle,nodeKinds,edgeVerbs} from './relation-layout.mjs';
import {renderDomainReader,focusSourceData} from './domain-reader.mjs';
/* Read-only views of declared prerequisites and source-backed relationships. */
const labels = {satisfied:'前提已满足',unsatisfied:'前提未满足',unknown:'尚待核实',stale:'依据过期',not_applicable:'不适用'};
const kinds = {task:'任务',epic:'专题',asset:'资产',document:'资料',condition:'条件',rule:'规则',material:'材料',outcome:'成果',milestone:'里程碑',flow:'流程定义',step:'动作'};
const verbs = {contains:'归属',supports:'支撑',requires:'需要',governed_by:'受约束于',defined_in:'定义于',verified_by:'由其验证',accepted_by:'由其接受',references:'引用',delegates_to:'委托职责',produces:'生产',consumes:'消费',defines:'定义',provides_policy:'提供政策'};
const authorities = {effective:'生效约定',proposed:'待议约定',reference:'参考资料',historical:'历史记录',unknown:'采用性质未核实'};
const tones = {satisfied:'good',unsatisfied:'bad',unknown:'muted',stale:'attention',not_applicable:'muted'};

const statusOf = value => labels[value] || value || '未声明判断';
const sourceKey = (node, lookup) => {const key=node?.record_key || lookup.get(node?.source_key)?.record_key;return key && lookup.recordKeys?.has(key) ? key : null;};
const sourceButton = (node, lookup, esc, label='打开定义原文') => sourceKey(node,lookup) ?
  `<button class="quiet" data-record="${esc(sourceKey(node,lookup))}" data-source-fragment="${esc(node?.ref?.fragment || lookup.get(node?.key)?.ref?.fragment || '')}">${esc(label)}</button>` : '<span class="notice">尚无可定位的原文</span>';
const pill = (value, esc, label=statusOf(value)) => `<span class="relation-status ${tones[value] || 'muted'}">${esc(label)}</span>`;

function formula(expr, lookup, esc) {
  if (!expr) return '<p class="relation-note">尚未声明前提表达式。</p>';
  const children = expr.all || expr.any;
  if (children) return `<div class="requirement-expression"><strong>${expr.all ? '全部适用项须满足' : '任一适用分支满足即可'}</strong>${pill(expr.state,esc)}<ul>${children.map(child => `<li>${formula(child,lookup,esc)}</li>`).join('')}</ul></div>`;
  const node = lookup.get(expr.key);
  return `<div class="requirement-leaf"><button data-relation-node="${esc(expr.key || '')}" ${expr.key ? '' : 'disabled'}>${esc(node?.title || (expr.step ? `前置动作 ${expr.step}` : '未定位的条件'))}</button>${pill(expr.state,esc)}<p>${esc(expr.reason || '依据待核对')}</p></div>`;
}

function conditionDetails(condition, lookup, esc) {
  const expected = condition.expected_check;
  const origin = lookup.get(condition.source_key);
  const kind = expected?.kind === 'decision' ? (expected.actor_kind === 'user' ? '用户决定' : '范围明确的决定') : expected?.kind === 'evidence' ? '验证证据' : '尚未绑定判断方式';
  return `<div class="condition-detail"><div class="relation-detail-title"><h4>${esc(condition.title)}</h4>${pill(condition.state,esc)}</div>
    <p>${esc(kind)} · ${esc(condition.action || '动作未限定')}</p><p>${esc(condition.reason || '尚无判断理由')}</p>
    <dl class="relation-facts"><dt>采用性质</dt><dd>${esc(condition.authority || '未知')} / ${esc(condition.strength || '未限定')}</dd><dt>作用范围</dt><dd>${esc(condition.scope || '未限定')}</dd></dl>
    ${sourceButton(condition,lookup,esc,'打开条件定义')}
    ${(condition.proofs || []).length ? `<ul class="relation-proofs">${condition.proofs.map(proof => `<li><strong>${esc(proof.title || '证明记录')}</strong><span>${esc(proof.actor?.kind || '身份未核实')}${proof.actor?.id ? ` / ${esc(proof.actor.id)}` : ''}</span><p>${esc(proof.conclusion || '')}</p>${proof.record_key && lookup.recordKeys?.has(proof.record_key) ? `<button class="quiet" data-record="${esc(proof.record_key)}">打开证明原文</button>` : '<p>证明原文尚未登记。</p>'}</li>`).join('')}</ul>` : '<p class="relation-note">没有相符的证明。材料存在或任务关闭不会代替此项判断。</p>'}</div>`;
}

function relationDeclaration(edge, lookup, esc) {
  if (!edge.authority) return '';
  const origin = lookup.get(edge.source_key);
  return `<p class="relation-note">原声明：${esc(authorities[edge.authority] || edge.authority)}</p>${sourceButton({...origin,ref:{...origin?.ref,fragment:edge.definition_id||edge.id||''}},lookup,esc,'打开关系定义')}`;
}

function directRelations(related, lookup, esc) {
  return `<section class="inspector-section"><h4>直接关系</h4>${related.length ? `<ul class="inspector-links">${related.map(({edge,key,inbound}) => `<li><span>${inbound?'指入此对象':'此对象指向'} · ${esc(edge.label || verbs[edge.relation] || edge.relation)}</span><button data-relation-node="${esc(key)}">${esc(lookup.get(key).title)}</button>${relationDeclaration(edge,lookup,esc)}</li>`).join('')}</ul>` : '<p>尚无已登记的直接关系。</p>'}</section>`;
}

function inspector(node, flow, g, lookup, esc) {
  if (!node) return '<aside class="relation-inspector"><h3>选择一个节点</h3><p>查看适用范围、前提和原始依据。</p></aside>';
  const step = flow?.steps?.find(item => item.key === node.key);
  const condition = g.conditions?.find(item => item.key === node.key);
  const incoming = (g.edges || []).filter(edge => edge.to === node.key && lookup.has(edge.from));
  const outgoing = (g.edges || []).filter(edge => edge.from === node.key && lookup.has(edge.to));
  const related = [...incoming.map(edge => ({edge,key:edge.from,inbound:true})),...outgoing.map(edge => ({edge,key:edge.to,inbound:false}))];
  const target = lookup.get(step?.target_key);
  const origin = lookup.get(node.source_key) || node;
  return `<aside class="relation-inspector" aria-label="节点详情"><div class="inspector-heading"><span>${esc(kinds[node.kind] || '来源对象')}</span><h3>${esc(node.title)}</h3>${step ? pill(step.status,esc) : condition ? pill(condition.state,esc) : ''}</div>
    ${step ? `<p>${esc(step.reason)}</p><dl class="relation-facts"><dt>对应工作</dt><dd>${esc(target?.title || '尚未定位')}</dd><dt>动作</dt><dd>${esc(step.action)}</dd><dt>范围</dt><dd>${esc(flow.scope)}</dd></dl>${target ? `<button class="secondary" data-focus="${esc(target.key)}">定位对应工作</button>` : ''}
      <section class="inspector-section"><h4>声明的前提</h4>${formula(step.requires,lookup,esc)}</section>
      ${(step.condition_keys || []).length ? `<section class="inspector-section"><h4>判断依据</h4>${step.condition_keys.map(key => g.conditions.find(c => c.key === key)).filter(Boolean).map(c => conditionDetails(c,lookup,esc)).join('')}</section>` : ''}
      <section class="inspector-section"><h4>引用此结果的后续动作</h4>${step.affected_keys?.length ? `<ul class="inspector-links">${step.affected_keys.map(key => {const later=flow.steps.find(s => s.key===key);return later ? `<li><button data-relation-node="${esc(key)}">${esc(later.title)}</button>${pill(later.status,esc)}</li>` : '';}).join('')}</ul><p class="relation-note">各动作按自己的表达式判断；存在引用不代表全部阻断。</p>` : '<p>本流程未声明后续引用。</p>'}</section>` : condition ? conditionDetails(condition,lookup,esc) + directRelations(related,lookup,esc) :
      `<p>${esc(node.reason || '查看原记录中的职责和适用范围。')}</p>${node.status ? `<p>原状态：${esc(node.status)}</p>` : ''}${directRelations(related,lookup,esc)}`}
    <section class="inspector-section"><h4>原始来源</h4>${sourceButton(node,lookup,esc)}<details class="relation-provenance"><summary>来源位置与版本</summary><p>${esc(node.path || origin.path || '未定位')}</p><p>${esc(node.revision || origin.revision || '版本未知')}</p></details></section>
    <p class="relation-note">此视图解释原记录。前提满足不自动执行、接受或关闭工作。</p></aside>`;
}

function selectedFlow(g, focusKey, ui) {
  const flows = g.flows || [];
  return flows.find(f => f.key === ui.flowKey) || flows.find(f => f.steps.some(s => s.target_key === focusKey)) || (ui.scope==='all' ? flows[0] : null);
}

export function relationViewIdentity(g, focusKey, ui) {
  if(ui.mode==='sources'&&ui.domainFocus&&(ui.domainView||'tree')==='tree')return JSON.stringify(['sources','reader',ui.domainFocus,ui.scope,ui.scope==='related'?focusKey:null]);
  return JSON.stringify([ui.mode,ui.lens,ui.direction,ui.scope,ui.domainFocus,
    ui.mode==='progress' ? selectedFlow(g || {},focusKey,ui)?.key || null : null,
    ui.scope==='related' ? focusKey : null,ui.domainFocus?ui.domainView||'tree':null,
    ui.mode==='sources'&&ui.domainFocus&&ui.domainView==='graph'&&ui.focusOnly!==false?domainSelection(selectSources(g||{},focusKey,ui),ui.selectionKey):null]);
}

function domainSelection(data,key){return data.nodes.some(node=>node.key===key)?key:data.nodes.find(node=>!node.external&&node.record_key&&!node.source_key&&!node.navigation_parent_key)?.key||data.nodes.find(node=>!node.external&&node.record_key&&!node.source_key)?.key||data.nodes[0]?.key;}

function flowSelection(g, focusKey, ui) {
  const flow = selectedFlow(g,focusKey,ui);
  if (!flow) return {flow:null,nodes:[],edges:[],groups:[]};
  const lookup = new Map(flow.steps.map(step => [step.key,step]));
  let nodes = flow.steps;
  if (ui.scope === 'related') {
    const matches = nodes.filter(step => step.target_key === focusKey).map(step => step.key);
    if (!matches.length) return {flow,nodes:[],edges:[],groups:[],emptyReason:'所选流程未声明当前对象的动作。可选择相符流程，或查看已登记范围。'};
    if (matches.length) {
      const keep = new Set(matches), queue = [...matches];
      while (queue.length) {
        const step = lookup.get(queue.shift());
        for (const key of [...step.predecessor_keys || [],...step.affected_keys || []]) if (lookup.has(key) && !keep.has(key)) {keep.add(key);queue.push(key);}
      }
      nodes = nodes.filter(step => keep.has(step.key));
    }
  }
  const keys = new Set(nodes.map(node => node.key));
  const edges = nodes.flatMap(step => (step.predecessor_keys || []).filter(key => keys.has(key)).map(key => ({from:key,to:step.key,relation:'prerequisite',label:'前置结果'})));
  const groups = [...new Set(nodes.map(node => node.group || '未分组'))];
  return {flow,nodes:nodes.map(n=>({...n,kind:"step"})),edges,groups};
}

export function selectRelationData(g,focusKey,ui){return ui.mode==='progress'?flowSelection(g,focusKey,ui):selectSources(g,focusKey,ui);}
const pendingModels=new WeakMap();let activeObserver;
function sourceOutline(node,lookup,esc){
  const children=[...lookup.values()].filter(n=>n.navigation_parent_key===node.key);
  const clauses=[...lookup.values()].filter(n=>n.source_key===node.key&&!['flow','step'].includes(n.kind));
  return `<section class="inspector-section"><h4>文档职责</h4><p>${esc(responsibility(node))}</p>${node.navigation_parent_key?`<p>收录入口：<button class="quiet" data-relation-node="${esc(node.navigation_parent_key)}">${esc(lookup.get(node.navigation_parent_key)?.title||'父来源未定位')}</button></p>`:''}</section>
    ${children.length?`<section class="inspector-section"><h4>收录文档 · ${children.length}</h4><ul class="inspector-links">${children.map(n=>`<li><button data-relation-node="${esc(n.key)}">${esc(n.title)}</button><span>${esc(responsibility(n))}</span></li>`).join('')}</ul><button class="quiet" data-relation-expand="${esc(node.key)}">在图中展开文档</button></section>`:''}
    ${node.headings?.length?`<section class="inspector-section"><h4>章节目录</h4><ul class="inspector-links">${node.headings.filter(h=>h.level>1).map(h=>`<li>${sourceButton({...node,ref:{...node.ref,fragment:h.fragment}},lookup,esc,h.text)}</li>`).join('')}</ul></section>`:''}
    ${clauses.length?`<section class="inspector-section"><h4>规则与具体条目 · ${clauses.length}</h4><ul class="inspector-links">${clauses.map(n=>`<li><button data-relation-node="${esc(n.key)}">${esc(n.title)}</button><span>${esc(nodeKinds[n.kind]||'原条目')}</span></li>`).join('')}</ul></section>`:''}`;
}
function domainInspector(group,data,lookup,esc){
  const nodes=data.nodes.filter(n=>n.group===group),records=data.flow?nodes:nodes.filter(n=>n.record_key&&!n.source_key);
  const members=new Set(nodes.map(n=>n.key)),cross=data.edges.filter(e=>members.has(e.from)!==members.has(e.to));
  return `<aside class="relation-inspector" aria-label="领域详情"><div class="inspector-heading"><span>领域归属</span><h3>${esc(group)}</h3><p>${records.length} ${data.flow?'个动作':'份来源'} · ${cross.length} 条跨组关系</p></div>${data.flow?'':`<button class="secondary" data-relation-domain-focus="${esc(group)}">聚焦此领域</button>`}<section class="inspector-section"><h4>原始文档与工作</h4><ul class="inspector-links">${records.map(n=>`<li><button data-relation-node="${esc(n.key)}">${esc(n.title)}</button><span>${esc(data.flow?n.action:responsibility(n))}</span></li>`).join('')}</ul></section><p class="relation-note">领域仅组织阅读；具体约束和判断仍在各原记录中。</p></aside>`;
}
function edgeInspector(edge,lookup,esc){
  return `<aside class="relation-inspector" aria-label="关系详情"><div class="inspector-heading"><span>${esc(edgeVerbs[edge.relation]||edge.relation)}</span><h3>${esc(edge.label)}</h3><p>${edge.members.length} 条原关系</p></div><section class="inspector-section"><h4>对应声明与引用</h4><ul class="inspector-links">${edge.members.map(e=>{const from=lookup.get(e.from),to=lookup.get(e.to);return `<li><button data-relation-node="${esc(e.from)}">${esc(from?.title||e.from)}</button><span>${esc(e.label||edgeVerbs[e.relation]||e.relation)} →</span><button data-relation-node="${esc(e.to)}">${esc(to?.title||e.to)}</button>${relationDeclaration(e,lookup,esc)}${!e.authority?sourceButton(from,lookup,esc,'打开对应原文'):''}</li>`;}).join('')}</ul></section><p class="relation-note">汇总保留每条原关系。导航归属与引用方向不构成执行顺序。</p></aside>`;
}
function diagram(data,ui,lookup,esc,selectedKey){
  const model=diagramModel(data,ui),proxy=model.representative(selectedKey);
  const groups=model.domainMode?model.groups.filter(g=>!g.collapsed).map(g=>`<section class="domain-boundary" data-layout-id="${esc(g.id)}"><div class="domain-heading"><button data-relation-domain="${esc(g.name)}"><strong>${esc(g.name)}</strong><span>${g.count} ${ui.mode==='progress'?'个动作':'份来源'}</span></button>${ui.mode==='sources'?`<button data-relation-domain-focus="${esc(g.name)}">聚焦</button>`:''}<button data-relation-collapse="${esc(g.id)}" aria-label="收起领域 ${esc(g.name)}" aria-expanded="true">收起</button></div></section>`).join(''):'';
  const cards=model.nodes.map(n=>{
    if(n.kind==='domain')return `<section class="domain-summary ${proxy===n.key?'selected':''}" data-layout-id="${esc(n.key)}"><button data-relation-domain="${esc(n.title)}"><strong>${esc(n.title)}</strong><span>${n.members.filter(key=>model.lookup.get(key)?.record_key&&!model.lookup.get(key)?.source_key).length} 份来源</span></button><div class="domain-preview">${n.members.map(key=>lookup.get(key)).filter(item=>item?.record_key&&!item.source_key).slice(0,2).map(item=>`<button data-relation-node="${esc(item.key)}">${esc(item.title)}</button>`).join('')}</div><button data-relation-collapse="${esc(n.key)}" aria-expanded="false">展开领域</button></section>`;
    const c=lookup.get(n.key),state=ui.mode==='progress'?n.status:c?.kind==='condition'?c.status:null;
    return `<article class="graph-node ${proxy===n.key?'selected':''} ${n.external?'external-node':''}" data-layout-id="${esc(n.key)}"><button class="graph-node-main" data-relation-node="${esc(n.key)}" aria-pressed="${proxy===n.key}"><span class="graph-node-kind">${esc(n.parentTitle?`收录于 ${n.parentTitle}`:nodeKinds[n.kind]||'原始文档')}${n.external?' · 外部关联':''}</span><strong>${esc(n.title)}</strong>${state?pill(state,esc):`<span class="graph-node-duty">${esc(ui.mode==='progress'?n.action:responsibility(n))}</span>`}</button>${n.childKeys?.length?`<button class="graph-node-expand" data-relation-expand="${esc(n.key)}" aria-expanded="${Boolean(ui.expanded?.has(n.key))}">${ui.expanded?.has(n.key)?'收起':'展开'}收录内容 · ${n.childKeys.length}</button>`:''}</article>`;
  }).join('');
  const lists=model.groups.map(g=>`<section><div class="between"><h3>${esc(g.name)}</h3>${ui.mode==='sources'?`<button class="quiet" data-relation-domain-focus="${esc(g.name)}">聚焦领域</button>`:''}</div>${data.nodes.filter(n=>n.group===g.name&&n.record_key&&!n.source_key).map(n=>`<button class="mobile-relation-node" data-relation-node="${esc(n.key)}"><strong>${esc(n.title)}</strong><span>${esc(nodeKinds[n.kind]||'文档')}</span></button>`).join('')}${ui.mode==='progress'?data.nodes.filter(n=>n.group===g.name).map(n=>`<button class="mobile-relation-node" data-relation-node="${esc(n.key)}"><strong>${esc(n.title)}</strong>${pill(n.status,esc)}</button>`).join(''):''}</section>`).join('');
  return {model,html:`<div class="relation-canvas" data-layout-ready="false" aria-label="完整关系画布"><p class="layout-message" role="status">正在安排文档与关系…</p><div class="diagram-size"><div class="diagram-board"><svg class="diagram-lines" aria-hidden="true"><defs><marker id="relation-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z"/></marker></defs><g class="routed-edges"></g></svg>${groups}${cards}<div class="graph-edge-labels"></div></div></div></div><div class="mobile-relations">${lists}</div>`};
}
export function renderRelations(g,focus,ui,{esc,recordKeys}){
  ui={mode:'sources',lens:'domains',direction:'DOWN',scope:'all',zoom:1,domainView:'tree',focusOnly:true,...ui};
  const lookup=new Map((g.nodes||[]).map(n=>[n.key,{...n,title:displayTitle(n)}]));lookup.recordKeys=recordKeys||new Set();
  for(const c of g.conditions||[])lookup.set(c.key,{...lookup.get(c.key),...c,status:c.state});
  const data=selectRelationData(g,focus?.key,ui);
  ui={...ui,collapsed:new Set(data.groups.map(name=>`domain:${name}`).filter(key=>!ui.openDomains?.has(key)))};
  for(const step of data.flow?.steps||[])lookup.set(step.key,{...lookup.get(step.key),...step,kind:'step'});
  const visibleKeys=new Set(data.nodes.map(n=>n.key));if(ui.mode==='progress')for(const n of data.nodes)for(const key of n.condition_keys||[])visibleKeys.add(key);
  const local=ui.mode==='sources'&&Boolean(ui.domainFocus),treeView=local&&ui.domainView==='tree';
  const selectedKey=local?domainSelection(data,ui.selectionKey):visibleKeys.has(ui.selectionKey)?ui.selectionKey:data.nodes.find(n=>n.key===focus?.key||n.target_key===focus?.key)?.key||data.nodes[0]?.key;
  const selected=lookup.get(selectedKey),diagramData=local?focusSourceData(data,selectedKey,ui.focusOnly):data,view=diagram(diagramData,local?{...ui,lens:'impact'}:ui,lookup,esc,selectedKey);
  const edge=view.model.edges.find(e=>e.key===ui.edgeKey);
  let detail=ui.domainSelection?domainInspector(ui.domainSelection,data,lookup,esc):edge?edgeInspector(edge,lookup,esc):inspector(selected,data.flow,g,lookup,esc);
  if(!ui.domainSelection&&!edge&&selected?.record_key&&ui.mode==='sources')detail=detail.replace('<section class="inspector-section"><h4>原始来源</h4>',`${sourceOutline(selected,lookup,esc)}<section class="inspector-section"><h4>原始来源</h4>`);
  const tabs=`<div class="relation-tabs" role="tablist" aria-label="关系视图"><button role="tab" id="relation-sources-tab" aria-controls="relation-view" aria-selected="${ui.mode==='sources'}" data-relation-mode="sources">规范来源</button><button role="tab" id="relation-progress-tab" aria-controls="relation-view" aria-selected="${ui.mode==='progress'}" data-relation-mode="progress">推进条件</button></div>`;
  const flowOptions=(g.flows||[]).map(f=>`<option value="${esc(f.key)}" ${data.flow?.key===f.key?'selected':''}>${esc(f.title)}</option>`).join('');
  const documentOptions=data.nodes.filter(node=>node.record_key&&!node.source_key).map(node=>`<option value="${esc(node.key)}" ${node.key===selectedKey?'selected':''}>${node.external?'外部 · ':''}${esc(node.title)}</option>`).join('');
  const graphControls=`<label class="flow-picker"><span>排列</span><select id="relation-direction"><option value="DOWN" ${ui.direction==='DOWN'?'selected':''}>纵向</option><option value="RIGHT" ${ui.direction==='RIGHT'?'selected':''}>横向</option></select></label><div class="relation-zoom"><button data-relation-zoom="out" aria-label="缩小关系图">−</button><button data-relation-zoom="reset" aria-label="重置缩放">重置缩放</button><button data-relation-zoom="in" aria-label="放大关系图">＋</button></div>`;
  const toolbar=local?(treeView?'':`<div class="relation-toolbar"><label class="flow-picker"><span>文档</span><select id="relation-document">${documentOptions}</select></label><button class="quiet" data-relation-focus-only aria-pressed="${ui.focusOnly}">当前文档关联</button>${graphControls}</div>`):`<div class="relation-toolbar">${ui.mode==='sources'?`<label class="flow-picker"><span>视角</span><select id="relation-lens"><option value="domains" ${ui.lens==='domains'?'selected':''}>项目领域</option><option value="impact" ${ui.lens==='impact'?'selected':''}>来源与影响</option></select></label>`:flowOptions?`<label class="flow-picker"><span>流程</span><select id="relation-flow">${flowOptions}</select></label>`:''}<div class="relation-scope"><button data-relation-scope="all" aria-pressed="${ui.scope==='all'}">已登记范围</button><button data-relation-scope="related" aria-pressed="${ui.scope==='related'}">当前关联</button></div>${graphControls}</div>`;
  const breadcrumb=local?`<div class="relation-breadcrumb"><button class="quiet" data-relation-domain-back>返回全局</button><span>全局 / ${esc(ui.domainFocus)}</span><div class="domain-view-tabs" role="tablist" aria-label="领域内视图"><button role="tab" id="domain-tree-tab" aria-controls="domain-detail-view" aria-selected="${treeView}" data-relation-domain-view="tree">文档树阅读器</button><button role="tab" id="domain-graph-tab" aria-controls="domain-detail-view" aria-selected="${!treeView}" data-relation-domain-view="graph">焦点关系图</button></div></div>`:'';
  const legend=ui.mode==='progress'?'箭头：原声明的前置结果':ui.lens==='domains'?'领域间连线汇总原关系；内部关系可聚焦查看':'箭头：文档级原关系；归属不表示执行顺序';
  const direct=(g.edges||[]).filter(edge=>edge.from===selectedKey||edge.to===selectedKey).flatMap(edge=>{const inbound=edge.to===selectedKey,key=inbound?edge.from:edge.to;return lookup.has(key)?[{edge,key,inbound}]:[];});
  const clauses=(g.nodes||[]).filter(node=>node.source_key===selectedKey&&['rule','condition','material'].includes(node.kind));
  const readerExtras=`<details class="reader-relations" data-reading-detail="reader-relations"><summary>关系与引用 · ${direct.length}</summary>${directRelations(direct,lookup,esc)}</details>${clauses.length?`<details class="reader-clauses" data-reading-detail="reader-clauses"><summary>条目与约束 · ${clauses.length}</summary><ul class="inspector-links">${clauses.map(node=>`<li><button data-relation-node="${esc(node.key)}">${esc(node.title)}</button><span>${esc(kinds[node.kind])}</span></li>`).join('')}</ul></details>`:''}${selected?.kind==='condition'?conditionDetails(g.conditions.find(condition=>condition.key===selectedKey),lookup,esc):''}`;
  const content=treeView?renderDomainReader(data,lookup,selectedKey,ui,{esc,sourceButton,extraDetails:readerExtras}):`<div class="relation-surface ${local?'domain-focus-surface':''}">${view.html}${detail}</div>`;
  const records=data.nodes.filter(node=>node.record_key&&!node.source_key),localCount=records.filter(node=>!node.external).length,externalCount=records.filter(node=>node.external).length;
  const localScope=local?`<span class="relation-scope-note">本领域 ${localCount} 份来源 · 外部关联 ${externalCount} 份${treeView?'':` · 当前图 ${diagramData.nodes.filter(node=>node.record_key&&!node.source_key).length} 份来源 / ${diagramData.edges.length} 条关系`}</span>`:'';
  const body=data.nodes.length?`${breadcrumb}<div class="relation-context"><strong>${esc(data.flow?.title||ui.domainFocus||(ui.lens==='impact'?'来源与影响':'项目领域关系图'))}</strong><span>${ui.mode==='progress'?data.nodes.length:data.nodes.filter(n=>n.record_key&&!n.source_key).length} ${ui.mode==='progress'?'个动作':'份来源'} · ${data.edges.length} 条原关系</span>${localScope}${data.flow?.authority&&data.flow.authority!=='effective'?'<span class="relation-status attention">此流程尚非生效约定</span>':''}</div><div ${local?`id="domain-detail-view" role="tabpanel" aria-labelledby="domain-${treeView?'tree':'graph'}-tab"`:''}>${content}</div><div class="relation-legend">${treeView?'文档树表示阅读收录；章节与关系均回读原记录':legend}${view.model.foldedInternal&&!treeView?` · ${view.model.foldedInternal} 条内部关系收录于折叠内容`:''}</div>`:`<div class="relation-empty"><h3>${ui.mode==='progress'?'尚无当前范围的推进流程':'尚无已登记来源'}</h3><p>${esc(data.emptyReason||'没有声明不表示前提满足。可从原文核对当前范围。')}</p>${ui.mode==='progress'?'<button class="secondary" data-relation-mode="sources">查看规范来源</button>':''}</div>`;
  const html=`<section class="relation-workspace" id="relation-workspace"><div class="relation-heading"><div><h2>文档关系与推进条件</h2><p>从领域找到文档，沿原关系核对职责、约束与依据。</p></div>${tabs}</div>${toolbar}<div id="relation-view" role="tabpanel" aria-labelledby="relation-${ui.mode==='progress'?'progress':'sources'}-tab">${body}</div></section>`;
  // Model is passed through a short-lived queue; it is not a second project record.
  renderRelations.current={model:view.model,ui,esc,selectedKey,treeView};return html;
}
export async function layoutRelations(root=document){
  const canvas=root.querySelector('.relation-canvas'),current=renderRelations.current;if(!canvas||!current){activeObserver?.disconnect();return;}
  const {model,ui,esc,selectedKey}=current;pendingModels.set(canvas,current);
  try{
    const layout=flattenLayout(await computeLayout(model,ui.direction));if(!canvas.isConnected||pendingModels.get(canvas)!==current)return;
    const board=canvas.querySelector('.diagram-board'),size=canvas.querySelector('.diagram-size'),svg=canvas.querySelector('svg');
    board.style.width=`${layout.width}px`;board.style.height=`${layout.height}px`;svg.setAttribute('width',layout.width);svg.setAttribute('height',layout.height);
    for(const el of board.querySelectorAll('[data-layout-id]')){const pos=layout.nodes.get(el.dataset.layoutId);if(pos){el.style.left=`${pos.x}px`;el.style.top=`${pos.y}px`;el.style.width=`${pos.width}px`;el.style.height=`${pos.height}px`;}}
    const byId=new Map(model.edges.map(e=>[e.id,e]));
    svg.querySelector('.routed-edges').innerHTML=layout.edges.map(e=>{const original=byId.get(e.id);if(!original)return '';const selected=original.members.some(m=>m.from===selectedKey||m.to===selectedKey)||original.key===ui.edgeKey;return (e.sections||[]).map(section=>{const pts=[section.startPoint,...section.bendPoints||[],section.endPoint];const d=pts.map((p,i)=>`${i?'L':'M'} ${p.x+e.offsetX} ${p.y+e.offsetY}`).join(' ');return `<g class="diagram-edge ${selected?'selected-edge':''} ${['references','defined_in','verified_by','accepted_by'].includes(original.relation)?'reference-edge':''}"><path d="${d}" marker-end="url(#relation-arrow)"/></g>`;}).join('');}).join('');
    board.querySelector('.graph-edge-labels').innerHTML=layout.edges.flatMap(e=>{const original=byId.get(e.id);return original?(e.labels||[]).map(label=>`<button class="graph-edge-label" data-relation-edge="${esc(original.key)}" data-label-x="${label.x+e.offsetX}" data-label-y="${label.y+e.offsetY}" data-label-width="${label.width}" data-label-height="${label.height}">${esc(label.text)}</button>`):[];}).join('');
    for(const el of board.querySelectorAll('[data-label-x]')){el.style.left=`${el.dataset.labelX}px`;el.style.top=`${el.dataset.labelY}px`;el.style.width=`${el.dataset.labelWidth}px`;el.style.height=`${el.dataset.labelHeight}px`;}
    const applyScale=()=>{const scale=Math.max(.8,Math.min(1,(canvas.clientWidth-28)/layout.width)*ui.zoom);board.style.transform=`scale(${scale})`;size.style.width=`${layout.width*scale}px`;size.style.height=`${layout.height*scale}px`;canvas.dataset.displayScale=scale.toFixed(3);};applyScale();
    canvas.dataset.layoutReady='true';canvas.querySelector('.layout-message').hidden=true;
    activeObserver?.disconnect();activeObserver=new ResizeObserver(applyScale);activeObserver.observe(canvas);
    canvas.dispatchEvent(new CustomEvent('relations-ready',{bubbles:true}));
  }catch(error){if(!canvas.isConnected)return;canvas.dataset.layoutReady='error';canvas.querySelector('.layout-message').textContent='关系画布暂未绘制；下方关系列表和原文仍可读取。';canvas.parentElement.classList.add('layout-failed');console.error('relationship layout failed',error);}
}
