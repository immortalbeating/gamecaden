/* Display projections only. Canonical identities, edges and states remain source-owned. */
export const nodeKinds={task:'任务',epic:'专题',asset:'资产',document:'文档',condition:'条件',rule:'规则',material:'材料',outcome:'成果',milestone:'里程碑',step:'动作'};
export const edgeVerbs={contains:'归属',supports:'支撑',requires:'需要',governed_by:'受约束于',defined_in:'定义于',verified_by:'由其验证',accepted_by:'由其接受',references:'引用',delegates_to:'委托职责',produces:'生产',consumes:'消费',defines:'定义',provides_policy:'提供政策',prerequisite:'前置结果'};
const roles={vision:'体验目标与项目边界',roadmap:'阶段范围与里程碑',spec:'规格与设计约定',rules:'工作方法与约束',task:'实施范围与工作记录',epic:'有界目标与所属工作',evidence:'验证范围与观察结果',decision:'对象、方面与判断',asset:'候选、用途与消费者',notes:'补充资料与上下文',index:'文档阅读入口'};
export const responsibility=node=>node.navigation_responsibility||roles[node.role]||roles[node.kind]||'职责尚未标注';
export const displayTitle=node=>node.kind==='document'&&/\.md$/i.test(node.title||'')?(node.headings?.find(h=>h.level===1)?.text||node.title):node.title;
export function domainOf(node,lookup){
  const owner=lookup.get(node.source_key);
  if(owner&&['rule','material','condition'].includes(node.kind))return domainOf(owner,lookup);
  if(node.navigation_domain||node.domain)return node.navigation_domain||node.domain;
  if(['task','epic','outcome','milestone'].includes(node.kind))return '开发工作';
  if(['evidence','decision'].includes(node.role))return '判断与证据';
  if(['asset','material'].includes(node.kind)||node.role==='asset-ledger')return '资产与交付';
  if(['vision','roadmap','index'].includes(node.role))return '方向与范围';
  if(['spec','rules'].includes(node.role))return '规范与设计';
  return '未分类资料';
}
export function selectSources(g,focusKey,ui){
  const lookup=new Map((g.nodes||[]).filter(n=>!['project','flow','step'].includes(n.kind)).map(n=>[n.key,n]));
  const allEdges=(g.edges||[]).filter(e=>lookup.has(e.from)&&lookup.has(e.to));
  let keep=new Set(lookup.keys());
  if(ui.domainFocus){
    keep=new Set([...lookup.values()].filter(n=>domainOf(n,lookup)===ui.domainFocus).map(n=>n.key));
    const inside=new Set(keep);for(const e of allEdges)if(inside.has(e.from)||inside.has(e.to)){keep.add(e.from);keep.add(e.to);}
  }else if(ui.scope==='related'&&lookup.has(focusKey)){
    keep=new Set([focusKey]);let frontier=[focusKey];
    for(let depth=0;depth<2&&frontier.length;depth++){
      const next=[];for(const e of allEdges)if(frontier.includes(e.from)||frontier.includes(e.to))for(const key of [e.from,e.to])if(!keep.has(key)){keep.add(key);next.push(key);}
      frontier=next;
    }
  }
  // Reading parents and definition owners keep a selected clause locatable.
  for(const key of [...keep]){let current=lookup.get(key),seen=new Set();while(current&&!seen.has(current.key)){seen.add(current.key);const parent=current.navigation_parent_key||current.source_key;if(!lookup.has(parent))break;keep.add(parent);current=lookup.get(parent);}}
  const nodes=[...lookup.values()].filter(n=>keep.has(n.key)).map(n=>({...n,title:displayTitle(n),group:domainOf(n,lookup),external:Boolean(ui.domainFocus&&domainOf(n,lookup)!==ui.domainFocus)}));
  return {flow:null,nodes,edges:allEdges.filter(e=>keep.has(e.from)&&keep.has(e.to)),groups:[...new Set(nodes.map(n=>n.group))],domainFocus:ui.domainFocus||null};
}
export function diagramModel(data,ui){
  const lookup=new Map(data.nodes.map(n=>[n.key,n])),parents=new Map(),children=new Map();
  const domainMode=ui.mode!=='progress'&&ui.lens!=='impact';
  for(const n of data.nodes){
    const owner=n.navigation_parent_key||(['rule','material','condition'].includes(n.kind)?n.source_key:null),parent=lookup.get(owner);
    if(parent&&parent.key!==n.key&&parent.group===n.group){parents.set(n.key,parent.key);if(!children.has(parent.key))children.set(parent.key,[]);children.get(parent.key).push(n.key);}
  }
  const groupKey=name=>ui.mode==='progress'?`progress:${data.flow?.key||''}:${name}`:`domain:${name}`;
  const representative=key=>{
    let current=key,walk=key,seen=new Set();
    while(parents.has(walk)&&!seen.has(walk)){seen.add(walk);const parent=parents.get(walk),documentOpen=ui.lens==='impact'&&Boolean(lookup.get(walk)?.navigation_parent_key);if(!documentOpen&&!ui.expanded?.has(parent))current=parent;walk=parent;}
    const n=lookup.get(current);return n&&domainMode&&ui.collapsed?.has(groupKey(n.group))?groupKey(n.group):current;
  };
  const visible=new Map(),groups=[];
  for(const name of data.groups){
    const members=data.nodes.filter(n=>n.group===name),key=groupKey(name),collapsed=domainMode&&ui.collapsed?.has(key);
    if(!members.length)continue;
    const sourceCount=members.filter(n=>n.record_key&&!n.source_key).length;
    groups.push({id:key,name,members:members.map(n=>n.key),count:sourceCount||members.length,collapsed});
    if(collapsed)visible.set(key,{key,kind:'domain',title:name,group:name,members:members.map(n=>n.key),external:members.every(n=>n.external),childCount:members.length});
    else for(const n of members)if(representative(n.key)===n.key)visible.set(n.key,{...n,childKeys:(children.get(n.key)||[]).filter(key=>ui.lens!=='impact'||!lookup.get(key)?.navigation_parent_key),parentTitle:lookup.get(parents.get(n.key))?.title});
  }
  const aggregated=new Map(),foldedOrigins=[];let foldedInternal=0;
  for(const e of data.edges){const from=representative(e.from),to=representative(e.to);if(!visible.has(from)||!visible.has(to))continue;if(from===to){foldedInternal++;foldedOrigins.push(e);continue;}
    const key=JSON.stringify([from,to,e.relation]);if(!aggregated.has(key))aggregated.set(key,{key,from,to,relation:e.relation,label:e.label||edgeVerbs[e.relation]||e.relation,members:[]});aggregated.get(key).members.push(e);
  }
  let edges=[...aggregated.values()],internalEdges=[];
  if(domainMode){const cross=new Map();for(const e of edges){const from=visible.get(e.from)?.kind==='domain'?e.from:groupKey(lookup.get(e.from).group),to=visible.get(e.to)?.kind==='domain'?e.to:groupKey(lookup.get(e.to).group);if(from===to){internalEdges.push(e);continue;}const key=JSON.stringify([from,to,e.relation]);if(!cross.has(key))cross.set(key,{...e,key,from,to,members:[]});cross.get(key).members.push(...e.members);}edges=[...cross.values()];}
  edges=edges.map((e,i)=>({...e,id:`edge-${i}`,label:e.members.length>1?`${e.label} · ${e.members.length} 条`:e.label}));
  return {nodes:[...visible.values()],edges,internalEdges,foldedOrigins,groups,domainMode,representative,children,foldedInternal,lookup};
}
const options=direction=>({'elk.algorithm':'layered','elk.direction':direction,'elk.edgeRouting':'ORTHOGONAL','elk.hierarchyHandling':'INCLUDE_CHILDREN','elk.padding':'[top=28,left=24,bottom=24,right=24]','elk.spacing.nodeNode':'32','elk.layered.spacing.nodeNodeBetweenLayers':'76','elk.spacing.edgeNode':'24','elk.spacing.edgeLabel':'12','elk.layered.nodePlacement.strategy':'NETWORK_SIMPLEX'});
export function layoutInput(model,direction='DOWN'){
  const nodes=model.nodes.map(n=>({id:n.key,width:n.kind==='domain'?236:210,height:n.kind==='domain'?182:n.childKeys?.length?156:132}));
  const graph={id:'relationship-root',layoutOptions:options(direction),children:[],edges:model.edges.map(e=>({id:e.id,sources:[e.from],targets:[e.to],labels:[{text:e.label,width:Math.max(52,e.label.length*14+16),height:24,layoutOptions:{'elk.edgeLabels.placement':'CENTER'}}]}))};
  if(model.domainMode)for(const group of model.groups){if(group.collapsed){graph.children.push(nodes.find(n=>n.id===group.id));continue;}const children=nodes.filter(n=>model.lookup.get(n.id)?.group===group.name);if(children.length)graph.children.push({id:group.id,width:258,height:76+children.reduce((h,n)=>h+n.height+18,0)});}
  else graph.children=nodes;
  return graph;
}
let engine;const cache=new Map();
export async function computeLayout(model,direction='DOWN',providedEngine){
  const graph=layoutInput(model,direction),key=JSON.stringify([graph,model.nodes.map(n=>[n.key,n.childKeys?.length||0])]);
  if(!providedEngine&&cache.has(key))return cache.get(key);
  const elk=providedEngine||(engine??=new globalThis.ELK());
  const promise=elk.layout(graph).then(result=>{if(model.domainMode)for(const group of model.groups){if(group.collapsed)continue;const box=result.children.find(n=>n.id===group.id);if(!box)continue;let y=72;box.children=model.nodes.filter(n=>model.lookup.get(n.key)?.group===group.name).map(n=>{const height=n.childKeys?.length?156:132;const child={id:n.key,x:24,y,width:210,height};y+=height+18;return child;});}return result;});if(!providedEngine){cache.set(key,promise);if(cache.size>16)cache.delete(cache.keys().next().value);promise.catch(()=>cache.delete(key));}
  return promise;
}
export function flattenLayout(graph){
  const nodes=new Map(),edges=[];
  function walk(parent,ox=0,oy=0){
    for(const n of parent.children||[]){const x=ox+(n.x||0),y=oy+(n.y||0);nodes.set(n.id,{...n,x,y});walk(n,x,y);}
    for(const e of parent.edges||[])edges.push({...e,offsetX:ox,offsetY:oy});
  }walk(graph);return {nodes,edges,width:graph.width,height:graph.height};
}

export function sourceRange(body,fragment){
  if(!fragment)return null;
  const matches=[];let offset=0,fence=null,governance=false;
  const identity=new RegExp('"id"\\s*:\\s*'+JSON.stringify(fragment).replace(/[.*+?^${}()|[\]\\]/g,'\\$&'));
  for(const line of body.split('\n')){
    const clean=line.trim();
    if(fence){if(new RegExp('^'+fence[0]+'{'+fence.length+',}\\s*$').test(clean))fence=null;offset+=line.length+1;continue;}
    if(clean==='<!-- workflow:governance -->')governance=true;
    else if(clean==='<!-- workflow:endgovernance -->')governance=false;
    else if(governance){if(identity.test(line))matches.push({start:offset,end:offset+line.length});}
    else {const opening=/^ {0,3}(`{3,}|~{3,})/.exec(line);if(opening)fence=opening[1];else {const heading=/^ {0,3}#{1,6}[ \t]+(.+?)\s*$/.exec(line);if(heading&&heading[1].replace(/[ \t]+#+[ \t]*$/,'')===fragment)matches.push({start:offset,end:offset+line.length});}}
    offset+=line.length+1;
  }
  return matches.length?{...matches[0],matches:matches.length}:null;
}
