/* Reconstructible browser reading state and source-change scheduling. No business facts live here. */
const viewFields=['page','selectedKey','selectedCandidateId','mediaIndex','sourceScroll','focusKey','taskRef','filters','conditionView','materialView','reviewFocus','comparison','relationMode','relationLens','relationDirection','relationScope','relationFlowKey','relationNodeKey','relationEdgeKey','relationDomain','relationDomainFocus','relationDomainView','relationFocusOnly','relationGlobalLens','relationZoom','relationCollapsed','relationExpanded','relationOpenDomains','relationMemory','documentFragment','documentReturn'];
export function captureView(state){
  const view=Object.fromEntries(viewFields.map(key=>[key,state[key]]));
  view.reader={nodeKey:state.relationReader?.nodeKey||null,fragment:state.relationReader?.fragment||''};
  return structuredClone(view);
}
export function applyView(state,view){
  if(!view)return;
  for(const key of viewFields)if(view[key]!==undefined)state[key]=structuredClone(view[key]);
  state.relationReader={nodeKey:view.reader?.nodeKey||null,fragment:view.reader?.fragment||'',record:null,loading:false,error:''};
}
export function changedSources(previous,next){
  const rows=value=>new Map((value?.source_revisions||[]).map(item=>[item.ref.path,item.revision]));
  const before=rows(previous),after=rows(next),paths=[...new Set([...before.keys(),...after.keys()])].filter(path=>before.get(path)!==after.get(path));
  return {paths,membershipChanged:[...before.keys()].some(path=>!after.has(path))||[...after.keys()].some(path=>!before.has(path))};
}
export function createRefreshCoordinator({context,readVersions,loadChanges,blocked,status=()=>{}}){
  const baselines=new Map(),dirty=new Map();let running=null,serial=0;
  const keyOf=bound=>JSON.stringify([bound.id,bound.binding]);
  const current=key=>keyOf(context())===key;
  const valid=value=>value?.complete===true&&typeof value.digest==='string'&&value.digest.length>0;
  function prime(bound,value,clearDirty=false){if(valid(value)){const key=keyOf(bound);baselines.set(key,value);if(clearDirty)dirty.delete(key);}}
  function invalidate(bound,recordKey=null){const key=keyOf(bound),old=dirty.get(key);dirty.set(key,{serial:++serial,keys:new Set([...(old?.keys||[]),recordKey].filter(Boolean))});}
  async function check(){
    if(running)return running;
    const bound={...context()},key=keyOf(bound);
    const work=(async()=>{
      let next;
      try{next=await readVersions(bound);}catch(error){if(current(key))status('error',error);return {kind:'error'};}
      if(!current(key))return {kind:'superseded'};
      if(!valid(next)){status('incomplete',next);return {kind:'incomplete'};}
      const previous=baselines.get(key),pending=dirty.get(key);
      if(previous?.digest===next.digest&&!pending){status('current');return {kind:'unchanged'};}
      if(blocked()){invalidate(bound);status('pending');return {kind:'deferred'};}
      const generation=dirty.get(key)?.serial||0;
      const changed=changedSources(previous,next);
      try{
        const result=await loadChanges(bound,{...changed,keys:[...(dirty.get(key)?.keys||[])],expected:next});
        if(!current(key))return {kind:'superseded'};
        if(!valid(result)){status('incomplete',result);return {kind:'incomplete'};}
        baselines.set(key,result);
        if((dirty.get(key)?.serial||0)===generation)dirty.delete(key);
        status(dirty.has(key)?'pending':'updated');return {kind:'updated'};
      }catch(error){if(current(key))status('error',error);return {kind:'error'};}
    })();
    running=work;
    try{return await work;}finally{if(running===work)running=null;}
  }
  return {prime,invalidate,check,pending:()=>dirty.has(keyOf(context())),baseline:bound=>baselines.get(keyOf(bound))||null};
}
