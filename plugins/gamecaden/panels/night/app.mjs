import {renderRelations,layoutRelations,relationViewIdentity} from './relations.mjs';
import {domainOf,sourceRange} from './relation-layout.mjs';
import {captureView,applyView,createRefreshCoordinator} from './panel-refresh.mjs';
const app = document.querySelector('#app');
const dialog = document.querySelector('#confirm');
const state = {session:null, csrf:null, projectId:null, page:'overview', records:[], diagnostics:[],
  selectedKey:null, selectedCandidateId:null, recordSelection:0, candidateSelection:0, reviewSelection:0,
  detail:null, candidate:null, mediaIndex:0, sourceScroll:0, queue:[], drafts:{}, pending:[], busy:false, complete:true,
  governance:null, governanceError:'', focusKey:null, taskRef:null, previewEpoch:0, conditionView:'current', filters:{domain:'all',action:'all',state:'all'},
  comparison:null, gallery:{}, galleryLoading:false, focusPreviewLoading:null, reviewFocus:null, reviewPreview:null, materialView:'current', governanceStale:false, relationMode:'sources', relationLens:'domains', relationDirection:'DOWN', relationScope:'all', relationFlowKey:null, relationNodeKey:null, relationEdgeKey:null, relationDomain:null, relationDomainFocus:null, relationDomainView:'tree',relationFocusOnly:true,relationReader:{nodeKey:null,fragment:'',record:null,loading:false,error:''},readerSelection:0,relationZoom:1, relationCollapsed:new Set(), relationExpanded:new Set(), relationOpenDomains:new Set(), relationMemory:new Map(), documentFragment:'', documentReturn:false, refreshMessage:'',readingRestore:null, message:'', error:''};
const projectViews=new Map();
const previewRequests=new Map();

const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const project = () => state.session?.projects?.find(p => p.id === state.projectId);
const base = () => `/api/projects/${encodeURIComponent(state.projectId)}`;
const endpoint = (...parts) => `${base()}/${parts.map(encodeURIComponent).join('/')}`;
const storageKey = name => `workflow-night:${state.projectId}:${project()?.binding_id || 'unbound'}:${name}`;
const loadStore = (name, fallback) => {try {return JSON.parse(localStorage.getItem(storageKey(name))) ?? fallback;} catch {return fallback;}};
const store = (name, value) => localStorage.setItem(storageKey(name), JSON.stringify(value));
const persist = () => {store('drafts', state.drafts); store('queue', state.queue); store('pending', state.pending);};
const issue = error => error?.message || String(error);
const navIcon = page => {
  const paths={overview:'<path d="M3 11 12 3l9 8M5 10v11h14V10M9 21v-7h6v7"/>',assets:'<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8" cy="8" r="1.5"/><path d="m3 17 5-5 4 4 4-6 5 7"/>',review:'<rect x="5" y="4" width="14" height="18" rx="2"/><path d="M9 4V2h6v2m-6 9 2 2 5-5"/>',documents:'<path d="M14 2H5v20h14V7Zm0 0v5h5M8 11h8m-8 4h8m-8 4h5"/>'};
  return `<svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[page]||''}</svg>`;
};
const shortVersion = value => {
  const raw=value?.value||(typeof value==='string'?value:'');
  return raw?`${value?.kind?value.kind+':':''}${raw.length>24?raw.slice(0,14)+'…'+raw.slice(-6):raw}`:'版本待核对';
};
function mediaMarkup(item,alt='候选预览') {
  const url=esc(endpoint('media',item.key));
  if(item.mime?.startsWith('image/'))return `<img src="${url}" alt="${esc(alt)}">`;
  if(item.mime?.startsWith('audio/'))return `<audio controls preload="none" aria-label="${esc(alt)}" src="${url}">浏览器无法播放此音频。</audio>`;
  if(item.mime?.startsWith('video/'))return `<video controls preload="metadata" aria-label="${esc(alt)}" src="${url}">浏览器无法播放此视频。</video>`;
  return `<a href="${url}" target="_blank" rel="noopener">打开媒体文件</a>`;
}

async function api(path, {method='GET', body=null, csrf=true}={}) {
  const headers = {};
  if (body !== null) headers['Content-Type'] = 'application/json';
  if (method !== 'GET' && csrf) headers['X-CSRF-Token'] = state.csrf;
  let response;
  try {response = await fetch(path, {method, headers, credentials:'same-origin', body:body === null ? undefined : JSON.stringify(body)});}
  catch (cause) {throw Object.assign(new Error('网络未连接；请求内容与编号已保留'), {network:true, cause});}
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw Object.assign(new Error(data.error?.message || `HTTP ${response.status}`),
    {code:data.error?.code || 'http_error', details:data.error?.details, status:response.status});
  return data;
}
const post = (path, body) => api(path, {method:'POST', body});
const notify = (message, error=false) => {state.message = error ? '' : message; state.error = error ? message : ''; render();};
const writeEnabled = capability => Boolean(project()?.capabilities?.[capability]);
const context = () => ({id:state.projectId, binding:project()?.binding_id});
const same = saved => saved.id === state.projectId && saved.binding === project()?.binding_id;
const boundBase = saved => `/api/projects/${encodeURIComponent(saved.id)}`;
function captureReadingDOM(){
  if(app.dataset.project!==state.projectId||app.dataset.page!==state.page)return null;
  const selectors=['.source-list','.relation-canvas','.relation-inspector','[data-reading-scroll="domain-tree"]','[data-reading-scroll="domain-reader"]','.document'];
  const active=document.activeElement;
  const focused=active?.id&&app.contains(active)?{id:active.id,owner:state.selectedKey,start:active.selectionStart,end:active.selectionEnd}:null;
  return {project:state.projectId,page:state.page,window:{left:window.scrollX,top:window.scrollY},focused,
    scrolls:selectors.flatMap(selector=>{const element=app.querySelector(selector);return element?[{selector,key:element.dataset.viewIdentity||element.dataset.readingKey||'',left:element.scrollLeft,top:element.scrollTop}]:[];}),
    details:[...app.querySelectorAll('details')].map(element=>({key:element.dataset.readingDetail||element.querySelector('summary')?.textContent,open:element.open,owner:state.selectedKey}))};
}
function restoreReadingDOM(reading){
  if(!reading||reading.project!==state.projectId||reading.page!==state.page)return;
  for(const saved of reading.details||[]){const element=[...app.querySelectorAll('details')].find(item=>(item.dataset.readingDetail||item.querySelector('summary')?.textContent)===saved.key);if(element&&(element.dataset.readingDetail||saved.owner===state.selectedKey))element.open=saved.open;}
  for(const saved of reading.scrolls||[]){const element=app.querySelector(saved.selector);if(element&&(element.dataset.viewIdentity||element.dataset.readingKey||'')===saved.key){element.scrollLeft=saved.left;element.scrollTop=saved.top;}}
  const focus=reading.focused;if(focus&&focus.owner===state.selectedKey){const element=document.getElementById(focus.id);if(element&&!element.disabled){element.focus({preventScroll:true});if(typeof focus.start==='number'&&element.setSelectionRange)element.setSelectionRange(focus.start,focus.end);}}
  window.scrollTo(reading.window.left,reading.window.top);
}
function autoRefreshBlocked(){const active=document.activeElement;return state.busy||dialog.open||document.hidden||Boolean(active?.isContentEditable||active?.matches('textarea,input,select'));}
function refreshStatus(kind){
  state.refreshMessage=({current:'已登记来源未变化',updated:'已更新来源；阅读位置已保留',pending:'来源有更新，结束当前编辑后刷新',incomplete:'来源尚未完整核对，可手动刷新',error:'版本检查暂不可用，可手动刷新'})[kind]||'';
  const target=document.querySelector('#source-refresh-status');if(target)target.textContent=state.refreshMessage;
}
let sourceCheckTimer;
function scheduleSourceCheck(){clearTimeout(sourceCheckTimer);sourceCheckTimer=setTimeout(()=>{if(state.session&&!document.hidden)void refreshCoordinator.check();},180);}
async function locked(work) {
  if (state.busy) return;
  state.busy = true; render();
  try {return await work();} finally {state.busy = false; render();if(refreshCoordinator.pending())scheduleSourceCheck();}
}
const settled = result => result?.receipt ? result.receipt.phase === 'settled' : ['conflict','rejected'].includes(result?.status);
const succeeded = result => result?.status === 'ok' && result?.receipt?.phase === 'settled' && result?.receipt?.outcome === 'ok'
  && Array.isArray(result?.writes) && result.writes.length > 0
  && result.writes.every(write => ['written','unchanged'].includes(write.status));

async function connect() {
  const params = new URLSearchParams(location.hash.slice(1));
  const token = params.get('connect');
  params.delete('connect');
  if (token) history.replaceState(null, '', location.pathname + location.search + (params.size ? `#${params}` : ''));
  const data = token ? await api('/api/connect', {method:'POST', body:{token}, csrf:false}) : await api('/api/session');
  state.session = data;
  state.csrf = data.csrf_token;
  const chosen = data.projects?.some(p => p.id === params.get('project')) ? params.get('project') :
    data.projects?.some(p => p.id === data.default_project_id) ? data.default_project_id : data.projects?.[0]?.id;
  if (!chosen) throw new Error('当前会话没有可查看的项目');
  state.page = ['overview','assets','review','documents'].includes(params.get('view')) ? params.get('view') : 'overview';
  state.taskRef = params.get('task');
  state.relationMode = ['progress','sources'].includes(params.get('diagram')) ? params.get('diagram') : 'sources';
  state.relationLens=params.get('lens')==='impact'?'impact':'domains';state.relationDirection=params.get('layout')==='RIGHT'?'RIGHT':'DOWN';
  state.relationFlowKey = params.get('flow'); state.relationNodeKey = params.get('node');state.relationDomainFocus=params.get('domain');state.relationDomainView=params.get('reader')==='graph'?'graph':'tree';
  state.initialRoute = {task:params.get('task'),asset:params.get('asset'),candidate:params.get('candidate')};
  await chooseProject(chosen, true);
}

function routeHash() {
  const params = new URLSearchParams();
  params.set('project',state.projectId); params.set('view',state.page);
  const focus = state.governance?.nodes?.find(n => n.key === state.focusKey && n.kind === 'task');
  const task = focus ? nodeRef(focus) : state.taskRef;
  if (task) params.set('task',task);
  if (state.page === 'overview') {params.set('diagram',state.relationMode);params.set('lens',state.relationLens);params.set('layout',state.relationDirection); if (state.relationFlowKey) params.set('flow',state.relationFlowKey); if (state.relationNodeKey) params.set('node',state.relationNodeKey);if(state.relationDomainFocus){params.set('domain',state.relationDomainFocus);params.set('reader',state.relationDomainView);}}
  const asset = state.records.find(r => r.key === state.selectedKey && r.record_type === 'asset');
  if (asset) params.set('asset',String(asset.metadata?.id || asset.title || ''));
  if (asset && state.selectedCandidateId) params.set('candidate',state.selectedCandidateId);
  history.replaceState(null,'',location.pathname + location.search + `#${params}`);
}

async function chooseProject(id, initial=false) {
  if (state.busy && state.projectId) return;
  if(state.projectId){rememberRelationView();projectViews.set(JSON.stringify([state.projectId,project()?.binding_id]),{view:captureView(state),reading:captureReadingDOM()});}
  state.projectId = id;
  state.filters = {domain:'all',action:'all',state:'all'}; state.conditionView = 'current'; state.materialView = 'current';
  if (!initial) {state.page = 'overview'; state.relationMode='sources';state.relationLens='domains';state.relationDirection='DOWN'; state.relationFlowKey=null; state.relationNodeKey=null;}
  state.relationScope='all';if(!initial)state.relationDomainFocus=null;state.relationDomainView=initial?state.relationDomainView:'tree';state.relationDomain=null;state.relationEdgeKey=null; state.relationZoom=1; state.relationCollapsed=new Set(['domain:开发工作','domain:判断与证据','domain:资产与交付']);state.relationExpanded=new Set();state.relationOpenDomains=new Set();state.relationMemory=new Map();state.documentFragment='';state.documentReturn=false;state.relationReader={nodeKey:null,fragment:'',record:null,loading:false,error:''};state.readerSelection++;state.refreshMessage='';state.readingRestore=null;
  state.selectedKey = null; state.selectedCandidateId = null;
  state.focusKey = null; if (!initial) state.taskRef = null; state.governance = null; state.governanceError = ''; state.governanceStale = false; state.comparison = null; state.gallery = {}; state.galleryLoading = false; state.focusPreviewLoading = null; state.reviewFocus = null; state.reviewPreview = null;
  state.recordSelection++; state.candidateSelection++; state.reviewSelection++; state.sourceScroll = 0; state.detail = null; state.candidate = null;
  state.records = []; state.diagnostics = []; state.complete = true;
  state.error = ''; state.message = '正在读取当前项目来源…';
  state.drafts = loadStore('drafts', {});
  state.queue = loadStore('queue', []).map(item => ({...item, scope:typeof item.scope === 'string' ? item.scope : ''}));
  state.pending = loadStore('pending', []);
  const saved=projectViews.get(JSON.stringify([id,project()?.binding_id]));if(!initial&&saved){applyView(state,saved.view);state.readingRestore=saved.reading;}
  await reload();
}

async function reload({automatic=false,expected=null,affectedKeys=[]}={}) {
  const bound = context();
  const reading=state.readingRestore||captureReadingDOM();rememberRelationView();state.readingRestore=reading;
  const prior=captureView(state),oldRecords=new Map(state.records.map(row=>[row.key,row])),oldBusy=state.busy;
  let before=expected,confirmed=null;
  state.busy=true;render();
  if(!before){try{before=await api(`${boundBase(bound)}/revisions`);}catch{state.refreshMessage='版本检查暂不可用；仍可手动读取来源。';}}
  if(!same(bound))return null;
  state.previewEpoch++; state.recordSelection++;state.candidateSelection++; state.reviewSelection++;state.readerSelection++;
  if(state.relationReader.loading){state.relationReader.loading=false;delete state.relationReader.attemptedRevision;}
  if(state.reviewPreview?.status==='loading')state.reviewPreview=null;
  state.galleryLoading = false; state.focusPreviewLoading = null;
  if(!automatic){state.gallery={};state.reviewPreview=null;}
  state.busy = true; render();
  try {
    let cursor = null, pages = 0, records = [], diagnostics = [], complete = true;
    do {
      const url = new URL(`${boundBase(bound)}/snapshot`, location.origin);
      if (cursor) url.searchParams.set('cursor', cursor);
      const data = await api(url.pathname + url.search);
      records.push(...(data.records || [])); diagnostics.push(...(data.diagnostics || []));
      complete = complete && data.complete !== false;
      cursor = data.next_cursor; pages += 1;
      if (pages > 10000) throw new Error('分页超过安全上限，请缩小项目范围');
    } while (cursor);
    if (!same(bound)) return;
    state.records = records; state.diagnostics = diagnostics; state.complete = complete;
    const changed=new Set([...affectedKeys,...records.filter(row=>oldRecords.get(row.key)?.revision!==row.revision).map(row=>row.key),...oldRecords.keys()].filter(key=>affectedKeys.includes(key)||!records.some(row=>row.key===key)||records.find(row=>row.key===key)?.revision!==oldRecords.get(key)?.revision));
    for(const key of Object.keys(state.gallery))if([...changed].some(recordKey=>key.startsWith(recordKey+':')))delete state.gallery[key];
    await refreshGovernance(state.initialRoute?.task || state.taskRef);
    if (!same(bound)) return;
    state.error = '';if(!automatic)state.message = `已读取 ${records.length} 条来源记录${complete ? '' : '；来源扫描不完整'}`;
    const preferred = records.find(row => row.record_type === 'task' && row.metadata?.status === 'active') || records.find(row => row.record_type === 'task') || records[0];
    const routedAsset = records.find(r => r.record_type === 'asset' && r.metadata?.id === state.initialRoute?.asset);
    if (routedAsset && state.initialRoute?.candidate) await selectCandidate(routedAsset.key,state.initialRoute.candidate, {page:state.page, review:state.page === 'review'});
    else if (routedAsset) state.selectedKey = routedAsset.key;
    else if (state.selectedKey && records.some(row => row.key === state.selectedKey)) {
      const row=records.find(row=>row.key===state.selectedKey);
      if(prior.selectedCandidateId&&(row.metadata?.candidates||[]).some(candidate=>candidate.id===prior.selectedCandidateId)){
        if(!automatic||changed.has(row.key)||!state.candidate)await selectCandidate(row.key,prior.selectedCandidateId,{page:prior.page});
      }else{if(prior.selectedCandidateId){state.selectedCandidateId=null;state.candidate=null;}if(!automatic||changed.has(row.key)||!state.detail)await selectRecord(row.key,false,prior.documentFragment||'');}
    }
    else if (preferred) await selectRecord(preferred.key, false);
    state.initialRoute = null; routeHash();
    state.page=prior.page;state.documentReturn=prior.documentReturn;state.documentFragment=state.selectedKey===prior.selectedKey?prior.documentFragment||'':'';state.mediaIndex=state.selectedCandidateId===prior.selectedCandidateId?prior.mediaIndex||0:0;
    if(state.relationReader.nodeKey&&changed.has(state.relationReader.record?.key)){state.relationReader.record=null;delete state.relationReader.attemptedRevision;}
    if(state.relationDomainFocus)await loadDomainReader(null,null,!automatic);
    if (state.page === 'assets') void loadGalleryBatch();
    const reviewMember=state.queue.find(item=>queueId(item)===state.reviewFocus)||state.queue[0];
    if (state.page === 'review'&&(!state.reviewPreview||changed.has(reviewMember?.key)))void loadReviewFocus();
    try{const after=await api(`${boundBase(bound)}/revisions`);if(before?.complete===true&&after.complete===true&&before.digest===after.digest&&!state.governanceError){confirmed=after;if(!automatic)refreshCoordinator.prime(bound,after,true);state.refreshMessage='已更新来源；阅读位置已保留';}else{state.refreshMessage='来源在读取期间变化或尚未完整核对；请重新读取。';state.governanceStale=true;}}catch{state.refreshMessage='版本检查暂不可用；本次原文读取不作为最新版本确认。';}
  } catch (error) {if (same(bound)) {state.error = issue(error); state.message = '';}}
  finally {state.busy=oldBusy;render();restoreReadingDOM(reading);state.readingRestore=null;}
  return confirmed;
}

async function loadDomainReader(nodeKey=null,fragment=null,force=false){
  if(state.page!=='overview'||state.relationMode!=='sources'||!state.relationDomainFocus||state.relationDomainView!=='tree')return;
  const key=nodeKey||renderRelations.current?.selectedKey||state.relationNodeKey,node=nodeByKey(key);if(!node)return;
  const owner=nodeByKey(node.source_key)||node,recordKey=node.record_key||owner.record_key;if(!recordKey)return;
  const reader=state.relationReader,chosen=fragment!==null?fragment:reader.nodeKey===key?reader.fragment:node.ref?.fragment||owner.headings?.find(heading=>heading.level>1)?.fragment||'';
  if(!force&&reader.nodeKey===key&&(reader.loading||reader.attemptedRevision===owner.revision)){if(fragment!==null&&chosen!==reader.fragment){reader.fragment=chosen;render();}return;}
  const bound=context(),request=++state.readerSelection;state.relationReader={nodeKey:key,fragment:chosen,record:reader.record?.key===recordKey?reader.record:null,loading:true,error:'',attemptedRevision:owner.revision};render();
  try{const record=await api(`${boundBase(bound)}/records/${encodeURIComponent(recordKey)}`);if(!same(bound)||request!==state.readerSelection)return;if(record.key!==recordKey)throw new Error('文档来源已变化，请刷新');state.relationReader.record=record;if(record.revision!==owner.revision){refreshCoordinator.invalidate(bound,recordKey);scheduleSourceCheck();}}
  catch(error){if(!same(bound)||request!==state.readerSelection)return;state.relationReader.error=issue(error);state.relationReader.record=null;}
  if(same(bound)&&request===state.readerSelection){state.relationReader.loading=false;render();}
}

async function refreshGovernance(focusRef=state.taskRef) {
  const bound = context();
  try {
    const url = new URL(`${boundBase(bound)}/governance`, location.origin);
    if (focusRef) url.searchParams.set('focus',focusRef);
    const next = await api(url.pathname + url.search);
    if (!same(bound)) return;
    const prior = state.focusKey;
    state.governance = next; state.governanceError = ''; state.governanceStale = false;
    state.focusKey = next.nodes?.some(n => n.key === prior) ? prior : next.focus ||
      next.nodes?.find(n => n.kind === 'task' && (n.ref === focusRef || n.ref?.id === focusRef || n.metadata?.id === focusRef))?.key ||
      next.nodes?.find(n => n.kind === 'task' && n.status === 'active')?.key || next.nodes?.find(n => n.kind === 'task')?.key || null;
    const task = next.nodes?.find(n => n.key === state.focusKey && n.kind === 'task');
    if (task) state.taskRef = nodeRef(task);
    void loadFocusPreview();
  } catch (error) {if (same(bound)) {state.governanceError = issue(error); state.governanceStale = true;}}
  render();
}

async function loadGalleryBatch() {
  if (state.galleryLoading || state.page !== 'assets') return;
  const bound = context(), epoch = state.previewEpoch;
  const batch = state.records.filter(r => r.record_type === 'asset' && r.interpretation === 'native')
    .flatMap(r => (r.metadata?.candidates || []).map(c => ({key:r.key,id:c.id})))
    .filter(({key,id}) => !state.gallery[`${key}:${id}`]).slice(0,6);
  if (!batch.length) return;
  state.galleryLoading = true;
  for (let start=0; start<batch.length; start+=2) {
    const results = await Promise.all(batch.slice(start,start+2).map(async ({key,id}) => {
      try {return [key,id,await api(`${boundBase(bound)}/candidates/${encodeURIComponent(key)}/${encodeURIComponent(id)}`)];}
      catch (error) {return [key,id,{load_error:issue(error),candidate_id:id,media:[]}];}
    }));
    if (!same(bound) || epoch !== state.previewEpoch) return;
    for (const [key,id,value] of results) state.gallery[`${key}:${id}`] = value;
    render();
  }
  if (same(bound) && epoch === state.previewEpoch) state.galleryLoading = false;
  render();
}

async function loadCandidatePreview(key,id) {
  const row=state.records.find(record=>record.key===key&&record.interpretation==='native');
  if(!row?.metadata?.candidates?.some(candidate=>candidate.id===id))return;
  const bound=context(),epoch=state.previewEpoch,selection=state.candidateSelection;
  const requestKey=JSON.stringify([bound.id,bound.binding,key,id]),request=(previewRequests.get(requestKey)||0)+1;
  const failedMessage=state.gallery[`${key}:${id}`]?.load_error;
  previewRequests.set(requestKey,request);
  let value;
  try{value=await api(`${boundBase(bound)}/candidates/${encodeURIComponent(key)}/${encodeURIComponent(id)}`);}
  catch(error){value={load_error:issue(error),candidate_id:id,media:[]};}
  if(!same(bound)||epoch!==state.previewEpoch||selection!==state.candidateSelection||request!==previewRequests.get(requestKey))return;
  state.gallery[`${key}:${id}`]=value;
  if(state.selectedKey===key&&state.selectedCandidateId===id){
    state.candidate=value.load_error?null:value;
    if(!value.load_error&&failedMessage&&state.error===failedMessage)state.error='';
  }
  render();
}

function focusAsset() {
  const g = state.governance;
  const node = g?.nodes?.find(n => n.key === state.focusKey);
  const edge = g?.edges?.find(e => e.from === node?.key && g.nodes.some(n => n.key === e.to && n.kind === 'asset') ||
    e.to === node?.key && g.nodes.some(n => n.key === e.from && n.kind === 'asset'));
  const asset = g?.nodes?.find(n => n.key === (edge?.from === node?.key ? edge?.to : edge?.from) && n.kind === 'asset');
  const row = state.records.find(r => r.key === asset?.record_key);
  return {asset,row,candidateId:row?.metadata?.candidates?.[0]?.id};
}

async function loadFocusPreview() {
  const {row,candidateId} = focusAsset();
  if (!row || !candidateId || state.gallery[`${row.key}:${candidateId}`]) return;
  const bound = context(), focusKey = state.focusKey, epoch = state.previewEpoch;
  const request = `${bound.id}:${bound.binding}:${epoch}:${focusKey}:${row.key}:${candidateId}`;
  if (state.focusPreviewLoading === request) return;
  state.focusPreviewLoading = request; render();
  let value;
  try {value = await api(`${boundBase(bound)}/candidates/${encodeURIComponent(row.key)}/${encodeURIComponent(candidateId)}`);}
  catch (error) {value = {load_error:issue(error),media:[]};}
  if (same(bound) && epoch === state.previewEpoch && state.focusKey === focusKey) state.gallery[`${row.key}:${candidateId}`] = value;
  if (state.focusPreviewLoading === request) state.focusPreviewLoading = null;
  render();
}

async function selectRecord(key, show=true, fragment='') {
  const bound = context();
  const selection = ++state.recordSelection;
  state.candidateSelection++; state.selectedCandidateId = null;
  const row = state.records.find(item => item.key === key);
  // A governance refresh can discover a newly written proof before the source list refreshes.
  const knownSource = state.governance?.nodes?.some(n => n.record_key === key);
  if (!row && !knownSource) {state.selectedKey = null; state.detail = null; render(); return;}
  state.selectedKey = key; state.documentFragment=fragment; state.detail = null; state.candidate = null; state.mediaIndex = 0; render();
  try {const detail = await api(`${boundBase(bound)}/records/${encodeURIComponent(key)}`);
    if (!same(bound) || selection !== state.recordSelection || state.selectedKey !== key) return;
    if (detail.key !== key) throw new Error('来源标识已变化，请刷新后重读');
    const recordIndex = state.records.findIndex(item => item.key === key);
    if (recordIndex < 0) state.records.push(detail); else state.records[recordIndex] = detail;
    state.detail = detail; if (show) state.page = 'documents'; state.error = ''; routeHash();}
  catch (error) {if (!same(bound) || selection !== state.recordSelection || state.selectedKey !== key) return;
    state.detail = null; state.error = issue(error);}
  render();
  if(show&&state.documentFragment)requestAnimationFrame(()=>document.querySelector(".source-anchor")?.scrollIntoView({block:"center"}));
}

async function selectCandidate(key, candidateId, {page='assets',review=false}={}) {
  const bound = context();
  const selection = ++state.candidateSelection;
  state.recordSelection++; state.selectedKey = key; state.selectedCandidateId = candidateId; state.candidate = null; state.mediaIndex = 0; render();
  try {const candidate = await api(`${boundBase(bound)}/candidates/${encodeURIComponent(key)}/${encodeURIComponent(candidateId)}`);
    if (!same(bound) || selection !== state.candidateSelection || state.selectedKey !== key || state.selectedCandidateId !== candidateId) return;
    state.candidate = candidate; state.gallery[`${key}:${candidateId}`] = candidate; state.page = page; state.error = '';
    if (review) addReview(false); routeHash();}
  catch (error) {if (!same(bound) || selection !== state.candidateSelection || state.selectedKey !== key || state.selectedCandidateId !== candidateId) return;
    state.candidate = null; state.gallery[`${key}:${candidateId}`]={load_error:issue(error),candidate_id:candidateId,media:[]}; state.error = issue(error);}
  render();
}

function shell(content) {
  const p = project();
  const options = state.session.projects.map(item => `<option value="${esc(item.id)}" ${item.id === state.projectId ? 'selected' : ''}>${esc(item.name)}</option>`).join('');
  app.innerHTML = `<header><div class="brand">Gamecaden</div><div class="top-controls"><label class="sr-only" for="project">项目</label><select id="project" ${state.busy?'disabled':''}>${options}</select><span class="pill">${esc(p?.kind === 'native' ? '原生项目' : '原文只读')}</span></div></header>
    <div class="shell"><nav class="primary-nav" aria-label="主导航">
      ${[['overview','总览'],['assets','资产'],['review','审阅'],['documents','资料']].map(([page,label])=>`<button id="nav-${page}" data-page="${page}" ${state.page===page?'aria-current="page"':''}>${navIcon(page)}<span class="nav-label">${label}</span></button>`).join('')}
    </nav><main id="main">${state.error ? `<div class="error" role="alert">${esc(state.error)}</div>` : ''}
    ${state.message ? `<p class="status-line" role="status">${esc(state.message)}</p>` : '<p class="status-line"></p>'}<p class="source-refresh-status" id="source-refresh-status" role="status">${esc(state.refreshMessage)}</p>${content}</main></div>`;
  app.dataset.project=state.projectId;app.dataset.page=state.page;
}

const recordTitle = row => row.title || row.metadata?.title || row.label || row.record_type;
const badge = row => row.interpretation === 'native' ? '<span class="pill">原生记录</span>' : '<span class="pill warn">原文只读</span>';
const status = row => row.metadata?.status ? `<span class="pill">源状态：${esc(row.metadata.status)}</span>` : '';
const typeLabel = kind => ({task:'任务 Task',epic:'专题 Epic',vision:'愿景',roadmap:'路线',spec:'规格',design:'设计',plan:'计划',
  decision:'决定',evidence:'证据',asset:'资产', 'asset-ledger':'资产账本',notes:'笔记','parking-lot':'待议',
  rule:'规则',index:'索引',handoff:'交接',external:'旧格式原文'})[kind] || kind;
const category = kind => ['task','epic'].includes(kind) ? 'work' :
  ['vision','roadmap','spec','design','plan','notes','parking-lot','rule','index','handoff','history'].includes(kind) ? 'design' :
  ['decision','evidence'].includes(kind) ? 'decision' : ['asset','asset-ledger'].includes(kind) ? 'asset' : 'other';
const relativePath = value => {
  const raw = String(value || '').replaceAll('\\','/');
  const root = String(project()?.root || '').replaceAll('\\','/').replace(/\/$/,'');
  return root && raw.toLowerCase().startsWith(`${root.toLowerCase()}/`) ? raw.slice(root.length+1) : raw.split('/').slice(-2).join('/');
};
const taskMode = row => row.record_type === 'task' && row.metadata?.mode ?
  ` · ${row.metadata.mode === 'quick' ? 'Quick 快改' : row.metadata.mode === 'standard' ? 'Standard 标准' : row.metadata.mode}` : '';

const nodeByKey = key => state.governance?.nodes?.find(n => n.key === key);
const nodeRef = node => (typeof node?.ref === 'string' ? node.ref : node?.ref?.id || node?.metadata?.id || node?.ref?.fragment) || node?.title || '';
const relationLabel = relation => ({contains:'包含',supports:'支撑',requires:'需要',governed_by:'受约束于',defined_in:'定义于',
  verified_by:'由其验证',accepted_by:'由其接受',references:'引用'})[relation] || relation;
const stateLabel = value => ({accept:'接受此范围',revise:'需要修改',reject:'不在此范围采用',defer:'暂不决定',verified:'已通过',invalid:'无效',unsupported:'不支持',
  required:'必须',conditional:'条件适用',optional:'可选',applies:'适用',
  satisfied:'已满足',unsatisfied:'未满足',unknown:'未知',stale:'证据过期',
  not_applicable:'不适用',located:'已定位',missing:'缺失',effective:'生效',proposed:'提议',reference:'参考',historical:'历史',
  planned:'计划中',active:'进行中',closed:'已关闭',cancelled:'已取消'})[value] || value || '未知';
function nodeButton(node, label='打开来源') {
  const source = node?.record_key || nodeByKey(node?.source_key)?.record_key;
  return source ? `<button class="quiet" data-record="${esc(source)}">${esc(label)}</button>` : '<span class="notice">未登记可打开的来源</span>';
}
function overview() {
  const g = state.governance;
  if (!g || state.governanceStale) return `<section class="page-heading"><h1>项目总览</h1><p>${esc(project()?.name)}</p></section><div class="warning">治理映射${state.governanceStale?'需要重新读取':'未加载'}：${esc(state.governanceError || '保存或读取后，旧条件结果不再作为当前状态展示')}。资料页仍可查看已登记来源。</div><button class="secondary" data-action="refresh-governance">重新读取治理视图</button>`;
  const nodes = g.nodes || [], edges = g.edges || [], conditions = g.conditions || [], materials = g.materials || [];
  const focus = nodeByKey(state.focusKey) || nodeByKey(g.focus) || nodes.find(n => n.kind === 'task') || nodes.find(n => n.kind === 'project');
  const roots = nodes.filter(n => ['outcome','milestone','epic','task'].includes(n.kind));
  const rank = {outcome:0,milestone:1,epic:2,task:3};
  const childrenOf = parent => edges.flatMap(e => {
    if (e.relation === 'contains' && e.from === parent.key) return [{node:roots.find(n => n.key === e.to),relation:'归属'}];
    if (e.relation !== 'supports') return [];
    const otherKey = e.from === parent.key ? e.to : e.to === parent.key ? e.from : null;
    const other = roots.find(n => n.key === otherKey);
    return other && rank[other.kind] > rank[parent.kind] ? [{node:other,relation:'支撑'}] : [];
  }).filter(x => x.node);
  const childKeys = new Set(roots.flatMap(n => childrenOf(n).map(x => x.node.key)));
  const top = roots.filter(n => !childKeys.has(n.key));
  const tree = (node, depth=0, seen=new Set(),relation='') => {
    if (depth > 7 || seen.has(node.key)) return '';
    const next = new Set(seen); next.add(node.key);
    const children = childrenOf(node);
    return `<li><button class="tree-node" data-focus="${esc(node.key)}" aria-current="${node.key===focus?.key}"><span>${relation ? `${esc(relation)} · ` : ''}${esc(node.kind === 'task' ? 'Task' : node.kind === 'epic' ? 'Epic' : node.kind === 'outcome' ? '成果' : '里程碑')}</span><strong>${esc(node.title)}</strong><small>${esc(nodeRef(node))} · ${esc(stateLabel(node.status))}</small></button>${children.length ? `<ul>${children.map(x => tree(x.node,depth+1,next,x.relation)).join('')}</ul>` : ''}</li>`;
  };
  const ownConditions = state.conditionView === 'all' ? conditions : conditions.filter(c => !focus || !c.applies_to?.length || c.applies_to.includes(focus.key));
  const domains = [...new Set(ownConditions.map(c => c.domain).filter(Boolean))];
  const actions = [...new Set(ownConditions.map(c => c.action).filter(Boolean))];
  const select = (field,values,label) => `<label for="condition-${field}">${label}<select id="condition-${field}" data-filter="${field}"><option value="all">全部</option>${values.map(value => `<option value="${esc(value)}" ${state.filters[field]===value?'selected':''}>${esc(field === 'state' ? stateLabel(value) : value)}</option>`).join('')}</select></label>`;
  const shown = ownConditions.filter(c => (state.filters.domain==='all'||c.domain===state.filters.domain) &&
    (state.filters.action==='all'||c.action===state.filters.action) && (state.filters.state==='all'||c.state===state.filters.state));
  const conditionEmpty=ownConditions.length?'<div class="empty">没有符合筛选的已识别条件。<button class="quiet" data-action="clear-conditions">清除筛选</button></div>':`<div class="empty"><p>${state.conditionView==='current'?'当前已读来源未识别出与此对象关联的条件。':'当前已读来源未识别出项目条件。'}这不表示前提已满足。</p>${state.conditionView==='current'?`<button class="quiet" data-condition-view="all">查看项目条件 · ${conditions.length} 项</button>`:''}</div>`;
  const {asset:relatedAsset,row:assetRecord,candidateId:firstCandidate} = focusAsset();
  const preview = firstCandidate ? previewMedia(galleryCandidate(assetRecord.key,firstCandidate)) : null;
  const shownMaterials = state.materialView === 'all' ? materials : materials.filter(m => m.applies_to?.includes(focus?.key));
  const unscopedCount = materials.filter(m => !m.applies_to?.length).length;
  const diag = [...new Map([...(g.diagnostics || []),...(state.diagnostics || [])].map(d => {
    const source = nodeByKey(d.source_key)?.path || d.path || d.target?.path || d.target || d.source?.path || d.source || d.source_key || '';
    return [JSON.stringify([d.code || '',source,d.message || d.reason || '']),d];
  })).values()];
  const coverage = g.coverage || {};
  const relationsMarkup = renderRelations(g,focus,{mode:state.relationMode,lens:state.relationLens,direction:state.relationDirection,scope:state.relationScope,flowKey:state.relationFlowKey,selectionKey:state.relationNodeKey,edgeKey:state.relationEdgeKey,domainSelection:state.relationDomain,domainFocus:state.relationDomainFocus,domainView:state.relationDomainView,focusOnly:state.relationFocusOnly,reader:state.relationReader,zoom:state.relationZoom,collapsed:state.relationCollapsed,expanded:state.relationExpanded,openDomains:state.relationOpenDomains},{esc,recordKeys:new Set(state.records.map(record=>record.key))});
  return `<section class="page-heading"><div class="between"><div><h1>${esc(g.project?.name || project()?.name || '项目总览')}</h1></div><div class="row"><button class="quiet" data-action="show-relations">查看关系</button><button class="secondary" data-action="reload">刷新</button></div></div>
    <p class="notice">${esc(g.project?.kind || project()?.kind)} · ${coverage.structured?'结构化映射':'尚无完整治理映射'} · ${coverage.records_complete && state.complete ? '来源扫描完整' : '来源扫描部分完成'} · 材料 ${coverage.materials_mapped?'已识别':'未完整识别'} / 条件 ${coverage.conditions_mapped?'已识别':'未完整识别'}</p>
    <details class="source-versions"><summary>来源与版本</summary><dl class="facts"><dt>项目根</dt><dd>${esc(g.project?.root || project()?.root || '未知')}</dd><dt>视图生成</dt><dd>${esc(g.generated_at || '未知')}</dd><dt>当前原记录</dt><dd>${esc(focus?.path || '未定位')}</dd><dt>Revision</dt><dd>${esc(focus?.revision || '未知')}</dd></dl></details></section>
    ${focus?`<section class="overview-current" aria-label="当前工作"><div><p class="task-meta">${focus.kind==='task'?'当前 Task':'当前对象'} · ${esc(nodeRef(focus))}</p><h2>${esc(focus.title)}</h2></div><div class="row"><button class="secondary" data-action="show-work">查看工作详情</button>${nodeButton(focus,'打开原记录')}</div></section>`:''}
    ${!coverage.structured ? '<div class="warning">此项目尚未完成材料与条件识别。下方只呈现已登记对象；未知不能视为通过。</div>' : ''}
    ${!coverage.records_complete || !state.complete ? '<div class="warning">来源不完整，当前关系和缺口仅覆盖已读取内容。</div>' : ''}
    ${diag.length ? `<details class="panel"><summary>来源诊断 · ${diag.length} 项</summary><ul>${diag.map(d => `<li>${esc(d.code || '诊断')}：${esc(d.message || d.reason || d)}</li>`).join('')}</ul></details>` : ''}
    ${g.flows?.length ? relationsMarkup : ''}<div class="governance-layout"><aside class="panel outcome-tree"><h2>成果树</h2>${roots.length ? `<ul>${(top.length ? top : roots).sort((a,b) => rank[a.kind]-rank[b.kind]).map(n => tree(n)).join('')}</ul>` : '<p class="notice">尚无可确认的成果与工作项；请到资料页查看原记录。</p>'}</aside>
    <div class="governance-main"><section class="focus-stage" id="current-work" tabindex="-1"><p class="task-meta">${esc(focus?.kind === 'task' ? '当前 Task' : '当前对象')} · ${esc(nodeRef(focus))}</p><h2>${esc(focus?.title || '尚未定位当前工作')}</h2>
      ${relatedAsset ? `<div class="focus-media">${preview?.mime?.startsWith('image/') ? `<img src="${esc(endpoint('media',preview.key))}" alt="${esc(relatedAsset.title)} 的关联候选预览">` : `<div class="focus-no-media">${firstCandidate && state.focusPreviewLoading ? '正在读取关联候选预览…' : firstCandidate ? '关联候选暂无可用图像预览。' : '关联资产尚无登记候选。'}</div>`}<button class="secondary" data-linked-asset="${esc(assetRecord?.key || '')}" ${firstCandidate ? `data-id="${esc(firstCandidate)}"` : ''}>进入关联资产 · ${esc(relatedAsset.title)}</button></div>` : '<div class="focus-no-media">当前对象没有已登记的关联资产；以来源与条件为准。</div>'}
      ${focus?.excerpt?.text ? `<div class="source-excerpt"><strong>原文摘录${focus.excerpt.heading ? ` · ${esc(focus.excerpt.heading)}` : ''}</strong><p>${esc(focus.excerpt.text)}</p></div>` : `<p>${esc(focus?.reason || focus?.metadata?.purpose || focus?.metadata?.summary || '此对象没有已登记的目标说明。')}</p>`}
      ${focus?.kind === 'rule' ? `<dl class="facts"><dt>规则层级</dt><dd>${esc(focus.layer || '未知')}</dd><dt>作用范围</dt><dd>${esc(focus.scope || '未说明')}</dd><dt>采用性质</dt><dd>${esc(stateLabel(focus.authority))}</dd></dl>` : ''}
      <div class="row">${focus ? nodeButton(focus,'打开原记录') : ''}<button class="secondary" data-action="copy">复制续接摘要</button></div></section>
      <section class="panel"><div class="between"><h2>相关条件</h2><div class="row"><button class="source-filter" data-condition-view="current" aria-pressed="${state.conditionView==='current'}">当前条件</button><button class="source-filter" data-condition-view="all" aria-pressed="${state.conditionView==='all'}">项目条件</button><span class="notice">显示 ${shown.length} / 已识别 ${ownConditions.length} 项</span></div></div>
      ${state.conditionView==='all' ? '<p class="notice">仅汇总已登记条件；每项按自己的适用对象与动作判断，不构成全项目统一阻断。</p>' : ''}
      ${ownConditions.length?`<div class="condition-filters">${select('domain',domains,'领域')}${select('action',actions,'动作')}${select('state',['satisfied','unsatisfied','unknown','stale','not_applicable'],'状态')}</div>`:''}
       ${shown.length ? `<div class="condition-table"><table><thead><tr><th>条件</th><th>领域 / 动作</th><th>依据</th><th>状态与证据</th></tr></thead><tbody>${shown.map(c => `<tr><td><button class="condition-focus" data-focus="${esc(c.key)}">${esc(c.title)}</button><small>${esc(c.scope || c.subject || '')}</small><small>适用于：${esc(c.applies_to?.map(k => nodeByKey(k)?.title || k).join('、') || '待确认')}</small></td><td>${esc(c.domain || '未分类')} / ${esc(c.action || '未分类')}</td><td>${esc(c.strength === 'required' ? '必须' : '建议')} · ${esc(stateLabel(c.authority))}</td><td><span class="pill ${c.state==='satisfied'?'good':c.state==='unsatisfied'?'danger':'warn'}">${esc(stateLabel(c.state))}</span><small>${esc(c.reason || '未提供原因')}</small><details><summary>依据与证明 · ${c.proofs?.length || 0}</summary>${nodeButton(c,'打开条件定义')}${c.proofs?.length ? `<ul class="proof-list">${c.proofs.map(p => `<li><strong>${esc(p.title || '来源证明')}</strong><small>记录 ${esc(p.ref?.id || 'ID 未提供')}${p.ref?.fragment ? ` / ${esc(p.ref.fragment)}` : ''} · ${esc(p.actor?.kind || '身份未知')}${p.actor?.id ? ` / ${esc(p.actor.id)}` : ''}</small><small>路径 ${esc(p.path || '未知')} · Revision ${esc(p.revision || '未知')}${p.event_scope ? ` · 方面 ${esc(p.event_scope)}` : ''}</small>${p.record_key ? `<button class="quiet" data-record="${esc(p.record_key)}">打开证明原文</button>` : '<span class="notice">未登记可打开的证明原文</span>'}</li>`).join('')}</ul>` : '<p class="notice">尚无证明记录。</p>'}</details></td></tr>`).join('')}</tbody></table></div>` : conditionEmpty}</section>
       <div class="overview-bottom"><section class="panel"><div class="between"><h2>材料职责矩阵</h2><div class="row"><button class="source-filter" data-material-view="current" aria-pressed="${state.materialView==='current'}">当前对象</button><button class="source-filter" data-material-view="all" aria-pressed="${state.materialView==='all'}">全部材料</button></div></div><p class="notice">材料定位不等于条件通过；${unscopedCount} 项未限定对象，需按领域和动作核对。</p>${shownMaterials.length ? `<ul class="gap-list">${shownMaterials.map(m => `<li><strong>${esc(m.title)}</strong><span class="pill ${m.state==='located'?'good':m.state==='missing'?'danger':'warn'}">${esc(stateLabel(m.state))}</span><p>${esc(m.domain || '领域未登记')} · ${(m.for_actions || []).map(esc).join('、') || '动作未限定'} · ${esc(stateLabel(m.applicability))} · ${esc(stateLabel(m.requirement))}</p><p>${esc(m.purpose || '用途未说明')}</p><p>对象：${esc(m.applies_to?.length ? m.applies_to.map(k => nodeByKey(k)?.title || k).join('、') : '未限定对象')}。${esc(m.reason || m.applicability_reason || '暂无定位说明')}</p><div class="row">${nodeButton({source_key:m.source_key},'打开要求来源')}${m.record_key ? nodeButton(m,'打开材料') : ''}</div></li>`).join('')}</ul>` : '<p class="notice">当前对象没有明确绑定的材料；切换“全部材料”检查未限定对象及其他领域。这里不表示材料齐备。</p>'}</section>
       </div></div></div>${!g.flows?.length ? relationsMarkup : ''}`;
}

function documents() {
  const p = project();
  const search = state.drafts.search || '';
  const activeCategory = state.drafts.category || 'all';
  const rows = state.records.filter(row => (activeCategory === 'all' || category(row.record_type) === activeCategory)
    && `${recordTitle(row)} ${row.record_type} ${relativePath(row.path)}`.toLowerCase().includes(search.toLowerCase()))
    .sort((a,b) => {
      const rank = row => ({work:0,design:1,decision:2,asset:3,other:4})[category(row.record_type)];
      const lifecycle = row => ({active:0,planned:1,closed:2,cancelled:3})[row.metadata?.status] ?? 4;
      return rank(a)-rank(b) || lifecycle(a)-lifecycle(b) || recordTitle(a).localeCompare(recordTitle(b),'zh-CN');
    });
  const filters = [['all','全部'],['work','Task / Epic'],['design','设计与方向'],['decision','决定 / 证据'],['asset','资产']]
    .map(([id,label]) => `<button class="source-filter" data-category="${id}" aria-pressed="${activeCategory===id}">${label}</button>`).join('');
  const entries = rows.map(row => `<button class="source-item" data-record="${esc(row.key)}" ${row.key===state.selectedKey?'aria-current="true"':''}>
      <span class="source-kind">${esc(typeLabel(row.record_type))}${esc(taskMode(row))}</span><strong>${esc(recordTitle(row))}</strong>
      <small>${esc(relativePath(row.path))}</small>${row.metadata?.status ? `<span class="source-status">源状态：${esc(stateLabel(row.metadata.status))}</span>` : ''}</button>`).join('');
  const diagnostics = state.diagnostics.length ? `<section class="warning"><strong>来源诊断</strong><ul>${state.diagnostics.map(d => `<li>${esc(d.code)}：${esc(d.message)}</li>`).join('')}</ul></section>` : '';
  const detail = state.detail ? renderDetail(state.detail) : `<div class="empty">选择一条来源记录，查看原文和可用操作。</div>`;
   return `<section class="heading"><div><h1>资料与原文</h1><p>${esc(p?.name)} · ${esc(p?.root)}</p>
    <p class="notice">本机绑定身份：${p?.actor ? `${esc(p.actor.kind)} / ${esc(p.actor.id)}` : '未绑定'} · 来源：${esc(p?.identity_source || '未提供')}。此会话不代表账号认证或真人审批。</p></div><div class="row"><button class="secondary" data-action="reload" ${state.busy ? 'disabled' : ''}>刷新来源</button></div></section>
    ${!state.complete ? '<div class="warning">来源扫描不完整。下方仅展示已读取记录，请查看来源诊断；记录数量不代表项目全部内容。</div>' : ''}${diagnostics}
    <div class="toolbar"><label class="sr-only" for="search">搜索记录</label><input id="search" placeholder="搜索标题、类型或相对路径" value="${esc(search)}"><span id="source-count" class="muted">当前筛选 ${rows.length} / 已读取 ${state.records.length} 条</span></div>
    <div class="overview-layout"><aside class="source-panel" aria-label="来源记录"><div class="source-filters">${filters}</div><div class="source-list">${entries || '<div class="empty">没有匹配的来源记录。</div>'}</div></aside>
    <section class="detail-column" aria-label="记录详情">${detail}</section></div>`;
}

function renderDetail(row) {
  const nativeTask = row.record_type === 'task' && row.interpretation === 'native' && writeEnabled('task_body_write');
  const draftKey = `task:${row.key}`;
  const draft = state.drafts[draftKey];
  const body = draft?.body ?? row.body ?? '';
  const technicalText = /\.(json|ya?ml)$/i.test(String(row.path || ''));
  const range=sourceRange(row.body||'',state.documentFragment);
  const sourceText=range?`${esc(row.body.slice(0,range.start))}<mark class="source-anchor">${esc(row.body.slice(range.start,range.end))}</mark>${esc(row.body.slice(range.end))}`:esc(row.body);
  const readerNode=state.governance?.nodes?.find(node=>node.record_key===row.key&&!node.source_key);
  const location=state.documentFragment?`<p class="notice">${range?`已定位：${esc(state.documentFragment)}${range.matches>1?' · 同名多处，请核对原文':''}`:`原条目未找到：${esc(state.documentFragment)}；请核对当前来源版本。`}</p>`:'';
  return `<div class="panel stack"><div><div class="between"><span class="eyebrow">${esc(typeLabel(row.record_type))}</span>${badge(row)}</div><h2>${esc(recordTitle(row))}</h2><p class="notice">来源：${esc(relativePath(row.path))}</p>
    <details><summary>完整来源与版本</summary><dl class="facts"><dt>完整路径</dt><dd>${esc(row.path)}</dd><dt>Revision</dt><dd>${esc(row.revision)}</dd><dt>Ref</dt><dd>${esc(JSON.stringify(row.ref))}</dd></dl></details></div>
    <div class="row">${state.documentReturn?'<button class="quiet" data-return-relations>返回文档关系图</button>':''}${readerNode?`<button class="quiet" data-document-reader="${esc(readerNode.key)}">在章节阅读器查看</button>`:''}</div>${location}
    ${row.body === null ? '<div class="warning">该来源没有可显示的文本正文。元数据按原始记录展示。</div>' :
      technicalText ? `<details ${range?'open':''}><summary>查看技术原文</summary><pre class="document">${sourceText}</pre></details>` : `<pre class="document">${sourceText}</pre>`}
    ${row.metadata ? `<details><summary>源元数据</summary><pre class="metadata">${esc(JSON.stringify(row.metadata,null,2))}</pre></details>` : ''}
    ${nativeTask ? `<form id="task-form" class="stack"><h3>仅编辑 Task 正文</h3>${draft && draft.base_revision !== row.revision ? `<div class="warning">来源 Revision 已变化。草稿基于 ${esc(draft.base_revision)}，请手动核对；当前表单不会自动升级草稿基准。<button class="quiet" type="button" data-rebase-task>核对当前来源</button></div>` : ''}<label for="task-body">正文草稿</label><textarea id="task-body" name="body">${esc(body)}</textarea>
      <div class="row"><button class="primary" type="submit">核对并保存正文</button><span class="notice">标题、状态与来源元数据保持原样。</span></div></form>` : '<p class="notice">此记录当前仅提供原文阅读。</p>'}</div>`;
}

function assetRows() {return state.records.filter(row => row.record_type === 'asset' && row.interpretation === 'native');}
const galleryCandidate = (key,id) => state.gallery[`${key}:${id}`];
const previewMedia = c => c?.media?.find(m => m.mime?.startsWith('image/')) || c?.media?.[0];
const thumb = (key,id) => {
  const candidate=galleryCandidate(key,id),item = previewMedia(candidate);
  return item?.mime?.startsWith('image/') ? `<img src="${esc(endpoint('media',item.key))}" alt="${esc(id)} 候选预览" loading="lazy">` : `<div class="no-thumb">${candidate?.load_error?'读取失败':!candidate?'尚未读取':item?.mime?.startsWith('audio/')?'音频候选':item?.mime?.startsWith('video/')?'视频候选':'暂无图像预览'}</div>`;
};
function assets() {
  const rows = assetRows();
  const cards = rows.map(row => {const candidates=row.metadata?.candidates || [];
    return `<article class="asset-family"><h2>${esc(recordTitle(row))}</h2><p>${esc(row.metadata?.id || '')} · ${esc(row.metadata?.purpose || '用途未登记')}</p>
      <div class="candidate-gallery">${candidates.map(c => `<div class="candidate-entry"><button id="candidate-${esc(encodeURIComponent(row.key))}-${esc(encodeURIComponent(c.id))}" class="candidate-tile" data-candidate="${esc(row.key)}" data-id="${esc(c.id)}" aria-pressed="${state.selectedKey===row.key && state.selectedCandidateId===c.id}">${thumb(row.key,c.id)}<strong>${esc(c.id)}</strong><small>技术：${esc(stateLabel(galleryCandidate(row.key,c.id)?.check?.status || 'unknown'))}</small></button>${galleryCandidate(row.key,c.id)?.load_error?`<p class="candidate-load-error">${esc(galleryCandidate(row.key,c.id).load_error)}</p><button class="quiet candidate-retry" data-retry-candidate="${esc(row.key)}" data-id="${esc(c.id)}">重试此预览</button>`:''}</div>`).join('') || '<p class="notice">尚无候选</p>'}</div></article>`;}).join('');
  const selected = state.candidate;
   const unloaded = rows.flatMap(r => (r.metadata?.candidates || []).map(c => `${r.key}:${c.id}`)).filter(key => !state.gallery[key]).length;
   return `<section class="heading"><div><h1>资产库</h1><p>以真实候选为单位浏览；技术检查、指定用途、接受依据和运行采用分别核对。</p></div><div class="row"><button class="secondary" data-action="reload">刷新来源</button>${unloaded ? `<button class="secondary" data-action="load-gallery" ${state.galleryLoading?'disabled':''}>${state.galleryLoading?'读取中…':`读取下一批预览（余 ${unloaded}）`}</button>` : ''}</div></section>
    ${!writeEnabled('decision_record') && !writeEnabled('asset_selection') ? '<div class="warning">当前项目只读，候选仍可查看。</div>' : ''}
    <div class="asset-catalog">${cards || '<div class="empty">当前来源没有原生资产记录。资料页可能仍有只读资产原文。</div>'}</div>
    ${selected ? candidateDetail(selected) : '<div class="empty">选择一个候选，查看大图、技术检查和用途。</div>'}`;
}

function mediaView(candidate) {
  const item = candidate.media?.[state.mediaIndex];
  if (!item) return '<div class="asset-media"><div class="empty">没有通过校验且可安全预览的媒体。可查阅 manifest 和源文件。</div></div>';
  const media=mediaMarkup(item,`${item.name}：${item.role}`);
  return `<div class="asset-media">${media}</div><p id="media-error" class="media-error" role="status"></p><div class="media-strip">${candidate.media.map((m,i) => `<button data-media="${i}" aria-pressed="${i===state.mediaIndex}">${esc(m.name)} · ${esc(m.role)}</button>`).join('')}</div>`;
}

function candidateDetail(c) {
  const check = c.check?.status || 'unsupported';
  const uses = c.selected_uses || [];
  const allUses = c.all_uses || [];
   const alternatives = (state.records.find(r => r.key === state.selectedKey)?.metadata?.candidates || []).filter(x => x.id !== c.candidate_id);
   const comparisonId=alternatives.some(item=>item.id===state.comparison?.id)&&state.comparison?.key===state.selectedKey?state.comparison.id:alternatives[0]?.id;
   const compared=comparisonId?galleryCandidate(state.selectedKey,comparisonId):null;
   return `<section class="panel stack candidate-detail"><div><div class="between"><h2>${esc(c.asset_id)} / ${esc(c.candidate_id)}</h2><span class="pill ${check==='verified'?'good':check==='invalid'?'danger':'warn'}">技术校验：${esc(stateLabel(check))}</span></div></div>
    ${check === 'verified' ? '<p class="notice">校验仅说明 manifest 与成员字节相符，不代表接受或运行采用。</p>' : `<div class="warning">${esc((c.check?.errors || []).map(e => `${e.code}: ${e.message}`).join('；') || '没有可用技术校验适配器')}</div>`}
    ${mediaView(c)}<dl class="facts"><dt>候选 ID</dt><dd>${esc(c.candidate_id)}</dd><dt>技术检查</dt><dd>${esc(stateLabel(check))}；${esc(c.check?.reason || '仅校验候选文件，不能推出接受结论')}</dd><dt>指定用途</dt><dd>${uses.length ? uses.map(u => esc(`${u.use_id} · ${u.runtime_id} / ${u.consumer} / ${u.purpose}`)).join('<br>') : '未指定'}</dd><dt>接受依据</dt><dd>${esc(c.acceptance?.status ? stateLabel(c.acceptance.status) : '未知：尚未查询正式接受记录')}</dd><dt>运行采用</dt><dd>${esc(c.runtime?.status ? stateLabel(c.runtime.status) : '未知：尚无运行采用证据')}</dd></dl>
    ${alternatives.length ? `<div><div class="between comparison-picker"><h3>候选对比</h3><label for="comparison-candidate">对比候选<select id="comparison-candidate">${alternatives.map(item=>`<option value="${esc(item.id)}" ${item.id===comparisonId?'selected':''}>${esc(item.id)}</option>`).join('')}</select></label></div><p class="notice">并排核对两个候选；结论仍按各自记录判断。</p><div class="compare-grid"><div>${thumb(state.selectedKey,c.candidate_id)}<strong>${esc(c.candidate_id)}</strong><p class="notice">技术：${esc(stateLabel(check))}</p></div><div><button data-candidate="${esc(state.selectedKey)}" data-id="${esc(comparisonId)}">${thumb(state.selectedKey,comparisonId)}<strong>${esc(comparisonId)} · 切换查看</strong></button><p class="notice">技术：${esc(stateLabel(compared?.check?.status||'unknown'))}</p>${compared?.load_error?`<p class="candidate-load-error">${esc(compared.load_error)}</p>`:''}${!compared||compared.load_error?`<button class="quiet" data-retry-candidate="${esc(state.selectedKey)}" data-id="${esc(comparisonId)}">${compared?.load_error?'重试此预览':'读取此预览'}</button>`:''}</div></div></div>` : ''}
    <details><summary>来源与版本</summary><dl class="facts"><dt>manifest</dt><dd>${esc(c.manifest_path)}</dd><dt>候选版本</dt><dd>${esc(JSON.stringify(c.version))}</dd><dt>账本 Revision</dt><dd>${esc(c.ledger_revision)}</dd><dt>账本路径</dt><dd>${esc(c.ledger_path)}</dd></dl></details>
    <div class="row"><button class="primary" data-add-review="${esc(state.selectedKey)}" ${!writeEnabled('decision_record') ? 'disabled' : ''}>加入审阅队列</button><button class="secondary" data-selection="${esc(state.selectedKey)}" ${!writeEnabled('asset_selection') || !allUses.length ? 'disabled' : ''}>指定既有用途</button></div>
    <p class="notice">指定用途只修改已有 use_id；它本身不构成接受或运行验证。</p></section>`;
}

const queueId = item => item.draft_id || `${item.key}:${item.candidate_id}`;
const sameVersion = (left,right) => JSON.stringify(left) === JSON.stringify(right);
async function loadReviewFocus() {
  if (state.page !== 'review') return;
  const item = state.queue.find(q => queueId(q) === state.reviewFocus) || state.queue[0];
  if (!item) {state.reviewPreview = null; render(); return;}
  const memberId = queueId(item);
  state.reviewFocus = memberId;
  if (state.reviewPreview?.memberId === memberId && state.reviewPreview.status === 'loading') return;
  const bound = context(), selection = ++state.reviewSelection;
  state.reviewPreview = {memberId,status:'loading'}; render();
  try {
    const candidate = await api(`${boundBase(bound)}/candidates/${encodeURIComponent(item.key)}/${encodeURIComponent(item.candidate_id)}`);
    if (!same(bound) || selection !== state.reviewSelection || state.page !== 'review' || state.reviewFocus !== memberId) return;
    const draft = state.queue.find(q => queueId(q) === memberId);
    if (!draft) return;
    state.gallery[`${item.key}:${item.candidate_id}`]=candidate;
    state.reviewPreview = {memberId,status:sameVersion(candidate.version,draft.version)&&candidate.ledger_revision===draft.revision ? 'ready' : 'changed',candidate};
  } catch (error) {
    if (!same(bound) || selection !== state.reviewSelection || state.page !== 'review' || state.reviewFocus !== memberId) return;
    state.reviewPreview = {memberId,status:'error',error:issue(error)};
  }
  render();
}
function review() {
  const index = Math.max(0,state.queue.findIndex(item => queueId(item) === state.reviewFocus));
  const focused = state.queue[index];
  const members = focused ? reviewMember(focused,index) : '<div class="empty">队列为空。到资产库选择候选加入审阅。</div>';
  const strip = state.queue.map((item,i) => {const cached=galleryCandidate(item.key,item.candidate_id),matched=cached?.check?.status==='verified'&&sameVersion(cached.version,item.version)&&cached.ledger_revision===item.revision;
    const media=matched?previewMedia(cached):null;
    return `<button id="review-member-${esc(encodeURIComponent(queueId(item)))}" class="review-queue-item" data-review-focus="${esc(queueId(item))}" aria-pressed="${i===index}">${media?.mime?.startsWith('image/') ? `<img src="${esc(endpoint('media',media.key))}" alt="">` : `<div class="no-thumb">${media?.mime?.startsWith('audio/')?'音频候选':media?.mime?.startsWith('video/')?'视频候选':'选择后读取预览'}</div>`}<strong>${esc(item.asset_id)} / ${esc(item.candidate_id)}</strong>${media?`<small>${media.mime?.startsWith('image/')?'已读缩略图':'已读媒体'} · 切换时核对预览</small>`:''}<small>${esc(item.scope || '方面待填写')} · ${esc(stateLabel(item.conclusion))}</small></button>`;}).join('');
  const pending = state.pending.map((p,index) => `<article class="card pending"><div class="between"><strong>${esc(p.label)}</strong><span class="pill ${p.phase==='settled'?'good':'warn'}">${esc(p.phase)}</span></div>
    <p class="notice">${esc(p.request_id)} · ${esc(p.kind)}</p>${p.result ? receipt(p.result, p.record, p.readback_error) : ''}
    <footer class="row"><button class="secondary" data-recover="${index}" ${p.phase==='settled'?'disabled':''}>查询原请求并恢复</button><button class="quiet" data-forget="${index}" ${p.phase!=='settled'?'disabled':''}>移除已结算条目</button></footer></article>`).join('');
  return `<section class="heading"><div><h1>审阅</h1><p>先核对当前候选，再填写方面、用途与意见；每项保留独立版本和 request_id。</p></div>
    <div class="row"><button class="primary" data-action="batch" ${!state.queue.some(item=>item.conclusion!=='defer') || !writeEnabled('decision_record') ? 'disabled' : ''}>准备批量审阅</button></div></section>
    <div class="members">${members}</div><section class="review-members"><div class="between"><h2>成员队列</h2><span class="notice">${state.queue.length} 项；逐项选择焦点</span></div><div class="member-strip">${strip || '<p class="notice">队列暂无成员。</p>'}</div></section>
    <section class="stack recovery-section"><div><h2>未决请求与回执</h2><p class="notice">断线后先查询原 request_id。未结算或查询不到回执时，可原样重试冻结载荷；查询不到不证明从未执行。</p></div><div class="grid">${pending || '<div class="empty">没有待恢复请求。</div>'}</div></section>`;
}

function reviewMember(item,index) {
  const row = state.records.find(r => r.key === item.key),identity=encodeURIComponent(queueId(item));
  const chosenUse = (item.all_uses || []).find(u => u.use_id === item.use_id);
  const useOptions = (item.all_uses || []).map(u => `<option value="${esc(u.use_id)}" ${u.use_id===item.use_id?'selected':''}>${esc(u.use_id)} · ${esc(u.consumer)} · ${esc(u.purpose)}</option>`).join('');
  const preview = state.reviewPreview?.memberId === queueId(item) ? state.reviewPreview : null;
  const media = preview?.status === 'ready' ? previewMedia(preview.candidate) : null;
  return `<article class="panel member"><div class="stack"><div><h2>${esc(recordTitle(row || {title:item.asset_id}))} · ${esc(item.candidate_id)}</h2><p class="notice">成员 ${index+1} / ${state.queue.length}</p><button class="secondary review-jump" data-review-jump="${index}">填写意见</button></div>
    <div class="review-preview">${preview?.status === 'changed' ? '<div class="warning">候选或来源版本变化，请重新核对。新预览暂不展示；草稿仍绑定原版本。</div>' : preview?.status === 'loading' || !preview ? '<div class="notice" role="status">正在读取当前候选预览…</div>' : preview?.status === 'error' ? `<div class="warning">读取候选失败：${esc(preview.error)}。</div><button class="secondary" data-retry-review>重试预览</button>` : media ? mediaMarkup(media,`${item.candidate_id} 审阅预览`) : '<div class="empty">此候选没有可用媒体预览；请按源文件与审阅方面判断。</div>'}</div><p id="review-media-error" class="media-error" role="status"></p>
    <details class="review-version-details" data-reading-detail="review-version:${esc(queueId(item))}"><summary>版本依据 · ${esc(shortVersion(item.version))}</summary><dl class="facts"><dt>候选完整版本</dt><dd>${esc(JSON.stringify(item.version))}</dd><dt>来源 Revision</dt><dd>${esc(item.revision)}</dd></dl></details><p class="notice">审阅方面可用自由文本；use_id 仅绑定已登记的用途。</p>
    <div class="row"><button class="secondary" data-refresh-review="${index}">核对当前候选</button><button class="quiet" data-remove-review="${index}">移出队列</button></div></div>
    <form id="review-form-${esc(identity)}" data-review-form="${index}"><div class="row"><label for="review-conclusion-${esc(identity)}">结论<select id="review-conclusion-${esc(identity)}" name="conclusion"><option value="defer" ${item.conclusion==='defer'?'selected':''}>延期（只存草稿）</option><option value="accept" ${item.conclusion==='accept'?'selected':''}>接受</option><option value="revise" ${item.conclusion==='revise'?'selected':''}>需修改</option><option value="reject" ${item.conclusion==='reject'?'selected':''}>不在此范围采用</option></select></label>
    <label for="review-use-${esc(identity)}">既有用途（可选）<select id="review-use-${esc(identity)}" name="use_id"><option value="">不绑定 use_id</option>${useOptions}</select></label></div>
    <p class="notice" data-use-facts>已绑定用途：${chosenUse ? esc(`${chosenUse.use_id} · ${chosenUse.runtime_id} / ${chosenUse.consumer} / ${chosenUse.purpose} / ${chosenUse.baseline || '无 baseline'}`) : '无，按对象和审阅方面记录'}</p>
    <label for="review-scope-${esc(identity)}">审阅方面<input id="review-scope-${esc(identity)}" name="scope" required maxlength="500" value="${esc(item.scope || '')}" placeholder="例如：外观与可读性"></label>
    <label for="review-note-${esc(identity)}">审阅说明<textarea id="review-note-${esc(identity)}" class="review-note" name="note" required>${esc(item.note || '')}</textarea></label>
    <p class="review-feedback">${item.conclusion==='defer'?'延期仅保留本地草稿；选择其他结论后可准备写回。':'准备后将核对范围、版本与写入内容。'}</p><button class="secondary" type="submit" ${item.conclusion==='defer'?'disabled':''}>${item.conclusion==='defer'?'延期无需提交':'准备此成员'}</button></form></article>`;
}

function receipt(result, record, readbackError) {
  const writes = result?.writes || [];
  const confirmed = succeeded(result);
  const label = confirmed ? record ? writes.some(w => w.status === 'written') ? '源文件写入并回读' : '回执已确认；相同字节已存在并回读'
    : '回执已确认；源记录待刷新' : '原库结果待核对或未写入';
  return `<div class="receipt"><strong class="${confirmed?'':'muted'}">${label}</strong>
    <div>outcome: ${esc(result?.receipt?.outcome || '无')} · phase: ${esc(result?.receipt?.phase || '无')} · response status: ${esc(result?.status)} · writes: ${esc(writes.map(w=>w.status).join(', ') || '无')}</div>
    ${result?.errors?.length ? `<pre>${esc(JSON.stringify(result.errors,null,2))}</pre>` : ''}${readbackError ? `<pre>回读错误：${esc(JSON.stringify(readbackError,null,2))}</pre>` : ''}${record ? `<div>回读 Revision：${esc(record.revision)}</div>` : ''}</div>`;
}

function render() {
  if (!state.session) return;
  const reading=state.readingRestore||captureReadingDOM();rememberRelationView();
  const oldList = document.querySelector('.source-list');
  if (oldList) state.sourceScroll = oldList.scrollTop;
  shell(state.page === 'assets' ? assets() : state.page === 'review' ? review() : state.page === 'documents' ? documents() : overview());
  const pane=relationScrollElement();if(pane)pane.dataset.viewIdentity=relationViewKey();
  layoutRelations(app);
  if (state.busy) app.querySelectorAll('button,input,select,textarea').forEach(control => { control.disabled = true; });
  const newList = document.querySelector('.source-list');
  if (newList) newList.scrollTop = state.sourceScroll;
  restoreReadingDOM(reading);
  if(app.querySelector('.domain-reader-layout')&&!state.governanceStale)void loadDomainReader();
}

function modal(title, body, onConfirm, label='确认提交') {
  dialog.innerHTML = `<div class="dialog-head"><h2 id="confirm-title">${esc(title)}</h2></div><div class="dialog-body">${body}</div>
    <div class="dialog-foot"><button class="secondary" data-dialog-cancel>返回修改</button><button class="primary" data-dialog-confirm>${esc(label)}</button></div>`;
  dialog.showModal();
  dialog.querySelector('[data-dialog-cancel]').onclick = () => dialog.close();
  dialog.querySelector('[data-dialog-confirm]').onclick = async () => {
    dialog.querySelector('[data-dialog-confirm]').disabled = true;
    dialog.close(); await onConfirm();
  };
}

function addPending(kind, path, payload, label, memberId=null,affectedKey=null) {
  const item = {kind, path, payload:structuredClone(payload), label, member_id:memberId,
    affected_key:affectedKey,request_id:payload.request_id, phase:'frozen', created_at:new Date().toISOString()};
  state.pending.unshift(item); persist(); render(); return item;
}
function settle(item, data) {
  item.result = data.result; item.record = data.record || null;
  item.readback_error = data.readback_error || null;
  item.phase = settled(data.result) ? 'settled' : 'unresolved';
  if (succeeded(data.result)) {state.governanceStale=true;refreshCoordinator.invalidate(context(),item.affected_key||item.record?.key||null);}
  if (item.kind === 'review' && succeeded(data.result) && item.member_id) {
    state.queue = state.queue.filter(q => queueId(q) !== item.member_id);
  }
  if (item.kind === 'task' && succeeded(data.result) && item.member_id && item.record?.body === item.payload.body
      && state.drafts[item.member_id]?.body === item.payload.body) delete state.drafts[item.member_id];
  persist(); render();
}
async function commit(item) {
  const bound = context();
  item.phase = 'transmitting'; persist(); render();
  try {const data = await post(item.path, item.payload); if (!same(bound)) return;
    settle(item, data); state.message = '已收到原库回执，请核对 status、writes 与回读。';}
  catch (error) {if (!same(bound)) return; item.phase = 'unresolved'; persist(); notify(`${item.label}：${issue(error)}。请在恢复区查询原请求。`, true);}
  render();
}

async function prepareTask(body) {
  const row = state.detail;
  if (!row || !writeEnabled('task_body_write')) return;
  const bound = context();
  const oldDraft = state.drafts[`task:${row.key}`];
  if (oldDraft?.base_revision && oldDraft.base_revision !== row.revision) return notify('来源已变化；请先核对当前来源与草稿，再明确更新草稿基准。', true);
  if (state.pending.some(p => p.kind === 'task' && p.member_id === `task:${row.key}` && p.phase !== 'settled'))
    return notify('此 Task 有未决保存请求，请先查询原 request_id。', true);
  state.drafts[`task:${row.key}`] = {body, base_revision:oldDraft?.base_revision || row.revision}; persist();
  try {
    const prepared = await post(`${boundBase(bound)}/task/prepare`, {key:row.key, revision:row.revision});
    if (!same(bound)) return;
    modal('核对 Task 正文写入', `<p>对象：${esc(recordTitle(row))}；来源版本：${esc(row.revision)}。作用范围仅为 Task 正文。</p><p>新正文：</p><pre>${esc(body)}</pre><details><summary>完整技术快照</summary><pre>${esc(JSON.stringify(prepared.preview,null,2))}</pre></details>`,
      async () => locked(async () => {
        if (!same(bound)) return;
        const payload = {ticket:prepared.ticket, request_id:crypto.randomUUID(), body};
        const item = addPending('task', `${boundBase(bound)}/task/save`, payload, `Task ${recordTitle(row)}`, `task:${row.key}`,row.key);
        await commit(item);
        if (same(bound) && succeeded(item.result) && item.record) {
          try {const updated = await api(`${boundBase(bound)}/records/${encodeURIComponent(row.key)}`);
            if (same(bound)) {state.detail = updated; delete state.drafts[`task:${row.key}`]; persist(); render();}}
          catch (error) {if (same(bound)) notify(`正文已写入，但刷新详情失败：${issue(error)}`, true);}
        }
      }), '保存正文');
  } catch (error) {notify(issue(error), true);}
}

function addReview() {
  const c = state.candidate;
  if (!c) return;
  const id = `${state.selectedKey}:${c.candidate_id}`;
  if (!state.queue.some(item => item.key === state.selectedKey && item.candidate_id === c.candidate_id)) {
    state.queue.push({key:state.selectedKey, asset_id:c.asset_id, candidate_id:c.candidate_id,
      draft_id:crypto.randomUUID(),
      revision:c.ledger_revision, version:c.version, all_uses:c.all_uses,
      use_id:'', scope:'',
      conclusion:'defer', note:''}); persist();
  }
  const member = state.queue.find(item => item.key === state.selectedKey && item.candidate_id === c.candidate_id);
  state.reviewFocus = member ? queueId(member) : null;
  state.page = 'review'; routeHash(); render(); window.scrollTo(0,0); void loadReviewFocus();
}

function captureMember(form) {
  const index = Number(form.dataset.reviewForm);
  const item = state.queue[index]; if (!item) return null;
  const values = new FormData(form);
  item.conclusion = values.get('conclusion'); item.note = values.get('note'); item.use_id = values.get('use_id');
  item.scope = String(values.get('scope') || '').trim();
  persist(); return item;
}
function reviewInput(item) {
  const payload = {asset_key:item.key, candidate_id:item.candidate_id, expected_revision:item.revision,
    expected_version:item.version, scope:item.scope};
  if (item.use_id) payload.use_id = item.use_id;
  return payload;
}

async function refreshReview(index) {
  const item = state.queue[index];
  if (!item) return;
  const memberId = queueId(item);
  if (state.pending.some(p => p.kind === 'review' && p.member_id === memberId && p.phase !== 'settled'))
    return notify('此成员有未决请求，请先恢复原 request_id，再核对新候选。', true);
  const bound = context();
  try {
    const current = await api(`${boundBase(bound)}/candidates/${encodeURIComponent(item.key)}/${encodeURIComponent(item.candidate_id)}`);
    if (!same(bound) || !state.queue.some(q => queueId(q) === memberId)) return;
    const oldUse = (item.all_uses || []).find(use => use.use_id === item.use_id) || null;
    const newUse = (current.all_uses || []).find(use => use.use_id === item.use_id) || null;
    const missingUse = Boolean(item.use_id && !newUse);
    const ledgerChanged = item.revision !== current.ledger_revision;
    const versionChanged = JSON.stringify(item.version) !== JSON.stringify(current.version);
    const usesChanged = JSON.stringify(item.all_uses || []) !== JSON.stringify(current.all_uses || []);
    const changes = [ledgerChanged ? '账本 Revision 已变化' : '账本 Revision 相同',
      versionChanged ? '候选版本已变化' : '候选版本相同',
      usesChanged ? '用途信息已变化' : '用途信息相同'];
    modal('核对当前候选与草稿基准', `<p>草稿结论、审阅方面和说明保持原样。${esc(changes.join('；'))}。</p>
      ${missingUse ? '<div class="warning">原 use_id 在当前账本中已不存在。确认后会解除此成员的 use_id 绑定，审阅方面与说明保持原样。</div>' : ''}
      <dl class="facts"><dt>旧账本 Revision</dt><dd>${esc(item.revision)}</dd><dt>当前账本 Revision</dt><dd>${esc(current.ledger_revision)}</dd>
      <dt>旧候选版本</dt><dd>${esc(JSON.stringify(item.version))}</dd><dt>当前候选版本</dt><dd>${esc(JSON.stringify(current.version))}</dd>
      <dt>原用途</dt><dd>${esc(oldUse ? JSON.stringify(oldUse) : item.use_id ? `已失去原用途详情：${item.use_id}` : '未绑定')}</dd>
      <dt>当前用途</dt><dd>${esc(newUse ? JSON.stringify(newUse) : item.use_id ? '原 use_id 不存在' : '未绑定')}</dd>
      <dt>全部用途变化</dt><dd>${esc(usesChanged ? `旧：${JSON.stringify(item.all_uses || [])}\n当前：${JSON.stringify(current.all_uses || [])}` : '无')}</dd>
      <dt>技术校验</dt><dd>${esc(current.check?.status || '未知')}</dd></dl>
      <p>草稿：${esc(item.conclusion)} · ${esc(item.scope)} · ${esc(item.note)}</p>`,
      async () => {
        if (!same(bound)) return;
        const target = state.queue.find(q => queueId(q) === memberId);
        if (!target) return;
        if (state.pending.some(p => p.kind === 'review' && p.member_id === memberId && p.phase !== 'settled'))
          return notify('此成员已有未决请求，先恢复原请求。', true);
        target.revision = current.ledger_revision;
        target.version = structuredClone(current.version);
        target.all_uses = structuredClone(current.all_uses || []);
        if (missingUse) target.use_id = '';
        if (state.reviewFocus === memberId) {
          state.reviewSelection++;
          state.reviewPreview = {memberId,status:'ready',candidate:current};
        }
        persist(); notify(missingUse ? '已更新候选基准，原 use_id 已解除；请核对范围。' : '已更新候选基准，草稿结论与说明未变。');
      }, '明确更新队列基准');
  } catch (error) {if (same(bound)) notify(`读取当前候选失败：${issue(error)}`, true);}
}

async function prepareReview(items) {
  const bound = context();
  const ready = [], failed = [];
  for (const item of items) {
    if (item.conclusion === 'defer') continue;
    if (!item.scope || !item.note?.trim()) {
      failed.push(`${item.candidate_id}：请填写审阅方面和说明`); continue;
    }
    if (state.pending.some(p => p.kind === 'review' && p.member_id === queueId(item) && (p.phase !== 'settled' || succeeded(p.result)))) {
      failed.push(`${item.candidate_id}：已有未决或成功请求，请先核对原回执`); continue;
    }
    try {
      const frozen = structuredClone(item);
      const prepared = await post(`${boundBase(bound)}/review/prepare`, reviewInput(frozen));
      if (!same(bound)) return;
      ready.push({item:frozen, prepared});
    } catch (error) {failed.push(`${item.candidate_id}：${issue(error)}`);}
  }
  if (!ready.length) {notify(failed.join('；') || '没有待提交结论；延期只保留草稿。', Boolean(failed.length)); return;}
   modal('逐项核对审阅快照', `<p>共 ${ready.length} 项准备完成。每项将使用独立 request_id 顺序提交；失败项保留草稿。</p>
     ${failed.length ? `<div class="warning">${esc(failed.join('；'))}</div>` : ''}
     ${ready.map(({item,prepared},i) => `<h3>${i+1}. ${esc(item.asset_id)} / ${esc(item.candidate_id)} · ${esc(stateLabel(item.conclusion))}</h3><p>候选版本：${esc(JSON.stringify(item.version))}。作用范围：${esc(item.scope)}${item.use_id ? ` / 用途 ${esc(item.use_id)}` : ' / 未绑定用途'}。意见：${esc(item.note)}</p><details><summary>完整技术快照</summary><pre>${esc(JSON.stringify(prepared.preview,null,2))}</pre></details>`).join('')}`,
    async () => locked(async () => {
      for (const {item,prepared} of ready) {
        if (!same(bound)) return;
        const payload = {ticket:prepared.ticket, request_id:crypto.randomUUID(), conclusion:item.conclusion, note:item.note};
        const pending = addPending('review', `${boundBase(bound)}/review/commit`, payload, `${item.asset_id} / ${item.candidate_id} 审阅`, queueId(item),item.key);
        await commit(pending);
      }
      state.page = 'review'; render();
    }), '逐项保存结论');
}

async function prepareSelection() {
  const c = state.candidate;
  if (!c || !writeEnabled('asset_selection')) return;
  const bound = context(), assetKey = state.selectedKey;
  const uses = c.all_uses || [];
  if (!uses.length) return notify('账本中没有可修改的既有 use_id。', true);
  modal('选择既有用途', `<p>指定 ${esc(c.candidate_id)} 到已有 use_id，不代表接受或运行验证。</p>
    <label for="select-use">既有 use_id<select id="select-use">${uses.map(u => `<option value="${esc(u.use_id)}">${esc(u.use_id)} · ${esc(u.consumer)} · ${esc(u.purpose)}</option>`).join('')}</select></label>`,
    async () => locked(async () => {
      const use_id = document.querySelector('#select-use')?.value || uses[0].use_id;
      const memberId = `selection:${assetKey}:${use_id}`;
      if (state.pending.some(p => p.kind === 'selection' && p.member_id === memberId && p.phase !== 'settled'))
        return notify('此用途有未决指定请求，请先查询原 request_id。', true);
      const input = {asset_key:assetKey, candidate_id:c.candidate_id, expected_revision:c.ledger_revision,
        expected_version:c.version, use_id};
      try {
        const prepared = await post(`${boundBase(bound)}/selection/prepare`, input);
        if (!same(bound)) return;
        modal('核对用途指定', `<p>对象：${esc(c.asset_id)} / ${esc(c.candidate_id)}；候选版本：${esc(JSON.stringify(c.version))}。作用范围仅为已有 use_id：${esc(use_id)}。本操作不构成接受或运行采用。</p><details><summary>完整技术快照</summary><pre>${esc(JSON.stringify(prepared.preview,null,2))}</pre></details>`,
          async () => locked(async () => {
            if (!same(bound)) return;
            const pending = addPending('selection', `${boundBase(bound)}/selection/commit`,
              {ticket:prepared.ticket, request_id:crypto.randomUUID()}, `${c.asset_id} / ${use_id} 用途指定`, memberId,assetKey);
            await commit(pending);
            if (same(bound) && succeeded(pending.result)) await selectCandidate(assetKey, c.candidate_id);
          }), '保存用途指定');
      } catch (error) {notify(issue(error), true);}
    }), '准备用途指定');
}

async function recover(index) {
  const item = state.pending[index]; if (!item || item.phase === 'settled') return;
  const bound = context();
  let retryReason = null;
  try {
    const checked = await post(`${boundBase(bound)}/operation/status`, {request_id:item.request_id});
    if (!same(bound)) return;
    const result = checked.result;
    if (result?.receipt) {
      item.result = result; item.phase = settled(result) ? 'settled' : 'unresolved';
      if (succeeded(result)) {state.governanceStale=true;refreshCoordinator.invalidate(context(),item.affected_key||item.record?.key||null);}
      if (item.kind === 'review' && succeeded(result) && item.member_id)
        state.queue = state.queue.filter(q => queueId(q) !== item.member_id);
      persist(); render();
      if (item.phase === 'settled') return notify(`原库已结算：${result.receipt.outcome || result.status}。请核对回执。`);
      retryReason = `原库回执阶段为 ${result.receipt.phase}；可用同一 request_id 和载荷继续原操作。`;
    } else {
      retryReason = result?.errors?.[0]?.code === 'not_found' ? '原库查询不到此 request_id；这不证明请求从未执行。' : null;
      if (!retryReason) return notify('状态查询没有可判断的 receipt，请保留冻结请求。', true);
    }
  } catch (error) {
    if (error.code !== 'not_found') return notify(`状态查询失败：${issue(error)}`, true);
    retryReason = '原库查询不到此 request_id；这不证明请求从未执行。';
  }
  if (retryReason && same(bound)) modal('确认继续原请求', `<p>${esc(retryReason)}</p><p>将原样发送冻结载荷：</p><pre>${esc(JSON.stringify(item.payload,null,2))}</pre>`,
    async () => locked(async () => {if (same(bound)) await commit(item);}), '发送原载荷');
}

const relationViewKey=()=>relationViewIdentity(state.governance,state.focusKey,{mode:state.relationMode,lens:state.relationLens,direction:state.relationDirection,scope:state.relationScope,domainFocus:state.relationDomainFocus,flowKey:state.relationFlowKey,domainView:state.relationDomainView,focusOnly:state.relationFocusOnly,selectionKey:state.relationNodeKey});
function relationScrollElement(){return app.querySelector('.relation-canvas')||app.querySelector('.domain-doc-tree');}
function rememberRelationView(){
  const pane=relationScrollElement();if(!pane||app.dataset.project!==state.projectId||app.dataset.page!==state.page)return;
  if(state.readingRestore||pane.matches('.relation-canvas')&&pane.dataset.layoutReady!=='true')return;
  const key=pane.dataset.viewIdentity||relationViewKey(),prior=state.relationMemory.get(key)||{};
  const view=key===relationViewKey()?{zoom:state.relationZoom,collapsed:new Set(state.relationCollapsed),expanded:new Set(state.relationExpanded),openDomains:new Set(state.relationOpenDomains)}:prior;
  state.relationMemory.set(key,{...prior,...view,left:pane.scrollLeft,top:pane.scrollTop,reading:captureReadingDOM()});
}
function switchRelationView(values){rememberRelationView();Object.assign(state,values);const saved=state.relationMemory.get(relationViewKey());state.relationZoom=saved?.zoom||1;state.relationCollapsed=new Set(saved?.collapsed||["domain:开发工作","domain:判断与证据","domain:资产与交付"]);state.relationExpanded=new Set(saved?.expanded||[]);state.relationOpenDomains=new Set(saved?.openDomains||[]);state.relationEdgeKey=null;state.relationDomain=null;state.relationRestoreViewport=saved?{left:saved.left,top:saved.top}:{left:0,top:0};state.readingRestore=saved?.reading||null;renderRelationChange();state.readingRestore=null;}
function revealRelationNode(key){const lookup=new Map((state.governance?.nodes||[]).map(n=>[n.key,n]));let node=lookup.get(key),seen=new Set();if(node){state.relationCollapsed.delete(`domain:${domainOf(node,lookup)}`);state.relationOpenDomains.add(`domain:${domainOf(node,lookup)}`);}while(node?.navigation_parent_key&&!seen.has(node.key)){seen.add(node.key);state.relationExpanded.add(node.navigation_parent_key);node=lookup.get(node.navigation_parent_key);}}
app.addEventListener('relations-ready',()=>{const saved=state.relationMemory.get(relationViewKey()),pane=relationScrollElement();if(saved&&pane){pane.scrollLeft=saved.left;pane.scrollTop=saved.top;}if(state.readingRestore)restoreReadingDOM(state.readingRestore);});
function renderRelationChange(kind, value) {
  const before=relationScrollElement();
  const scroll=state.relationRestoreViewport||{left:before?.scrollLeft || 0,top:before?.scrollTop || 0};state.relationRestoreViewport=null;
  state.relationMemory.set(relationViewKey(),{...state.relationMemory.get(relationViewKey()),...scroll,zoom:state.relationZoom,collapsed:new Set(state.relationCollapsed),expanded:new Set(state.relationExpanded),openDomains:new Set(state.relationOpenDomains)});
  routeHash(); render();
  const canvas=relationScrollElement();
  if (canvas) {canvas.scrollLeft=scroll.left; canvas.scrollTop=scroll.top;}
  const selector=kind==='node'?'[data-relation-node]':kind==='mode'?'[data-relation-mode][role=tab]':kind==='scope'?'[data-relation-scope]':kind==='collapse'?'[data-relation-collapse]':kind==='zoom'?'[data-relation-zoom]':null;
  const field={node:'relationNode',mode:'relationMode',scope:'relationScope',collapse:'relationCollapse',zoom:'relationZoom'}[kind];
  if (selector) [...document.querySelectorAll(selector)].find(button=>button.dataset[field]===value)?.focus({preventScroll:true});
}
app.addEventListener('keydown',event=>{
  const localTab=event.target.closest('[data-relation-domain-view][role=tab]');
  if(localTab&&['ArrowLeft','ArrowRight','Home','End'].includes(event.key)){event.preventDefault();const view=event.key==='Home'?'tree':event.key==='End'?'graph':state.relationDomainView==='tree'?'graph':'tree';switchRelationView({relationDomainView:view});document.querySelector(`[data-relation-domain-view="${view}"][role=tab]`)?.focus({preventScroll:true});return;}
  const tab=event.target.closest('[data-relation-mode][role=tab]');
  if (tab && ['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) {
    event.preventDefault();switchRelationView({relationMode:event.key==='Home'?'sources':event.key==='End'?'progress':state.relationMode==='progress'?'sources':'progress'});
    document.querySelector(`[data-relation-mode="${state.relationMode}"]`)?.focus({preventScroll:true});
  }
});

app.addEventListener('click', async event => {
  const button = event.target.closest('button'); if (!button) return;
  if (state.busy) return;
  if(button.dataset.action==='show-work'){const work=document.querySelector('#current-work');work?.scrollIntoView({block:'start'});work?.focus({preventScroll:true});return;}
  if(button.dataset.action==='clear-conditions'){state.filters={domain:'all',action:'all',state:'all'};render();return;}
  if(button.dataset.reviewJump!==undefined){const form=document.querySelector(`[data-review-form="${Number(button.dataset.reviewJump)}"]`);form?.scrollIntoView({block:'start'});form?.querySelector('select')?.focus({preventScroll:true});return;}
  if(button.hasAttribute('data-retry-review')){void loadReviewFocus();return;}
  if(button.dataset.retryCandidate)return loadCandidatePreview(button.dataset.retryCandidate,button.dataset.id);
  if(button.dataset.documentReader){const node=nodeByKey(button.dataset.documentReader),lookup=new Map((state.governance?.nodes||[]).map(n=>[n.key,n]));if(!node)return;if(!state.relationDomainFocus)state.relationGlobalLens=state.relationLens;state.page='overview';switchRelationView({relationMode:'sources',relationLens:'impact',relationScope:'all',relationDomainFocus:domainOf(node,lookup),relationDomainView:'tree',relationNodeKey:node.key});await loadDomainReader(node.key,state.documentFragment||'',true);document.querySelector('#relation-workspace')?.scrollIntoView({block:'start'});return;}
  if (button.dataset.action==='show-relations') {document.querySelector('#relation-workspace')?.scrollIntoView({block:'start'}); return;}
  if (button.dataset.relationMode) {switchRelationView({relationMode:button.dataset.relationMode});document.querySelector(`[data-relation-mode="${state.relationMode}"]`)?.focus({preventScroll:true}); return;}
  if(button.dataset.relationDomainView){switchRelationView({relationDomainView:button.dataset.relationDomainView==='graph'?'graph':'tree'});return;}
  if(button.hasAttribute('data-relation-focus-only')){switchRelationView({relationFocusOnly:!state.relationFocusOnly});return;}
  if(button.dataset.readerNode){switchRelationView({relationNodeKey:button.dataset.readerNode});revealRelationNode(state.relationNodeKey);renderRelationChange();return;}
  if(button.dataset.readerToggle){const key=button.dataset.readerToggle;if(state.relationExpanded.has(key))state.relationExpanded.delete(key);else state.relationExpanded.add(key);renderRelationChange();return;}
  if(button.hasAttribute('data-reader-chapter')){void loadDomainReader(null,button.dataset.readerChapter);return;}
  if(button.hasAttribute('data-reader-retry')){void loadDomainReader(null,null,true);return;}
  if (button.dataset.relationScope) {switchRelationView({relationScope:button.dataset.relationScope,relationDomainFocus:null}); return;}
  if (button.dataset.relationNode) {switchRelationView({relationNodeKey:button.dataset.relationNode});revealRelationNode(state.relationNodeKey);renderRelationChange('node',state.relationNodeKey);return;}
  if (button.dataset.relationEdge) {state.relationEdgeKey=button.dataset.relationEdge;state.relationDomain=null;renderRelationChange();return;}
  if (button.dataset.relationDomain) {state.relationDomain=button.dataset.relationDomain;state.relationEdgeKey=null;renderRelationChange();return;}
  if (button.dataset.relationDomainFocus) {if(!state.relationDomainFocus)state.relationGlobalLens=state.relationLens;switchRelationView({relationDomainFocus:button.dataset.relationDomainFocus,relationScope:'all',relationLens:'impact',relationDomainView:'tree',relationNodeKey:null});const lookup=new Map((state.governance?.nodes||[]).map(n=>[n.key,n]));for(const n of lookup.values())if(domainOf(n,lookup)===state.relationDomainFocus&&n.kind==='document')state.relationExpanded.add(n.key);renderRelationChange();return;}
  if (button.hasAttribute('data-relation-domain-back')) {switchRelationView({relationDomainFocus:null,relationLens:state.relationGlobalLens||'domains'});return;}
  if (button.dataset.relationExpand) {const key=button.dataset.relationExpand;if(state.relationExpanded.has(key))state.relationExpanded.delete(key);else state.relationExpanded.add(key);state.relationMemory.delete(relationViewKey());renderRelationChange();return;}
  if (button.dataset.relationCollapse) {const key=button.dataset.relationCollapse; if(state.relationOpenDomains.has(key))state.relationOpenDomains.delete(key);else state.relationOpenDomains.add(key); renderRelationChange('collapse',key); return;}
  if (button.dataset.relationZoom) {const action=button.dataset.relationZoom; state.relationZoom=action==='reset'?1:Math.max(.8,Math.min(1.8,Math.round((state.relationZoom+(action==='in'?.1:-.1))*10)/10));state.relationMemory.delete(relationViewKey()); renderRelationChange('zoom',action); return;}

  if (button.dataset.page) {state.page = button.dataset.page; routeHash(); render(); window.scrollTo(0,0);
    if (state.page === 'overview' && state.governanceStale) {scheduleSourceCheck();return;}
    if (state.page === 'assets') void loadGalleryBatch();
    if (state.page === 'review') void loadReviewFocus(); return;}
  if (button.dataset.focus) {const n = nodeByKey(button.dataset.focus);
    state.filters = {domain:'all',action:'all',state:'all'};
    if (n?.kind === 'task') state.taskRef = nodeRef(n);
    switchRelationView({focusKey:button.dataset.focus,relationFlowKey:null,relationNodeKey:null});
    void loadFocusPreview(); return;}
  if (button.dataset.linkedAsset !== undefined) {
    if (button.dataset.linkedAsset && button.dataset.id) return selectCandidate(button.dataset.linkedAsset,button.dataset.id);
    if (button.dataset.linkedAsset) state.selectedKey = button.dataset.linkedAsset;
    state.page = 'assets'; routeHash(); render(); void loadGalleryBatch(); return;
  }
  if (button.dataset.reviewFocus) {document.querySelectorAll('[data-review-form]').forEach(captureMember); state.reviewFocus = button.dataset.reviewFocus; state.reviewPreview = null; render(); void loadReviewFocus(); return;}
  if (button.dataset.materialView) {state.materialView = button.dataset.materialView; render(); return;}
  if (button.dataset.conditionView) {state.conditionView = button.dataset.conditionView; state.filters = {domain:'all',action:'all',state:'all'}; render(); return;}
  if (button.dataset.action === 'copy') {
    const focus = nodeByKey(state.focusKey);
    const g = state.governance;
    const cs = (g?.conditions || []).filter(c => c.applies_to?.includes(focus?.key));
    const ms = (g?.materials || []).filter(m => m.applies_to?.includes(focus?.key) && ['missing','unknown'].includes(m.state));
    const asset = state.records.find(r => r.key === state.selectedKey && r.record_type === 'asset');
    routeHash();
    const revisions = (g?.source_revisions || []).filter(s => !focus?.path || s.ref?.path === focus.path || s.ref?.path?.endsWith(focus.path));
    const source = revisions.length ? revisions : (g?.source_revisions || []).slice(0,3);
    const next = ms[0] ? `回读 ${ms[0].title} 的要求与来源，核对当前动作是否适用` :
      cs.find(c => ['unknown','stale','unsatisfied'].includes(c.state)) ? '回读相关条件的原要求与证明，核对对象、版本和现场' :
      '回读原 Task、Decision/Evidence 与实际工程状态，再按已有授权继续';
    const lines = [`项目：${project()?.name} (${state.projectId})`,`项目根：${g?.project?.root || project()?.root || '未知'}`,
      `派生时间：${g?.generated_at || '未知'}`,`当前范围：${focus?.kind === 'task' ? `Task ${nodeRef(focus)} ${focus.title}` : `${focus?.title || '未定位'}`}`,
      `原记录：${focus?.path || '未登记'}；Revision：${focus?.revision || '未知'}`,
      `来源版本：${source.length ? source.map(s => `${s.ref?.path || '路径未知'} @ ${s.revision || '未知'}`).join('；') : '未提供'}`,
      `相关条件：${cs.length ? cs.map(c => `${c.title}=${stateLabel(c.state)}`).join('；') : '未识别'}`,
      `材料缺口：${ms.length ? ms.map(m => `${m.title}=${stateLabel(m.state)}`).join('；') : '当前对象无明确绑定的缺口记录'}`,
      `候选：${asset ? `${asset.metadata?.id || recordTitle(asset)} / ${state.selectedCandidateId || '未选择'}` : '未选择'}`,
      `下一动作：${next}`,`深链接：${location.origin}${location.pathname}${location.search}${location.hash}`,
      '条件结果只表示记录依据，续接应重读原文、来源版本与现场；摘要不构成新授权。'];
    try {await navigator.clipboard.writeText(lines.join('\n')); notify('续接摘要已复制到剪贴板。');}
    catch {notify('复制失败，请检查浏览器剪贴板权限。',true);} return;
  }
  if (button.dataset.category) {state.drafts.category = button.dataset.category; state.sourceScroll = 0;
    document.querySelector('.source-list')?.scrollTo(0,0); persist(); render(); return;}
  if (button.hasAttribute('data-return-relations')) {const saved=state.relationMemory.get(relationViewKey());state.page='overview';state.readingRestore=saved?.reading||null;routeHash();render();state.readingRestore=null;if(!saved?.reading)document.querySelector('#relation-workspace')?.scrollIntoView({block:'start'});return;}
  if (button.dataset.record) {state.documentReturn=state.page==='overview';if(state.documentReturn)rememberRelationView();return selectRecord(button.dataset.record,true,button.dataset.sourceFragment||'');}
  if (button.dataset.candidate) return selectCandidate(button.dataset.candidate,button.dataset.id);
  if (button.dataset.media !== undefined) {state.mediaIndex = Number(button.dataset.media); render(); return;}
  if (button.dataset.addReview) return addReview();
  if (button.dataset.selection) return prepareSelection();
  if (button.dataset.refreshReview !== undefined) {
    const form = document.querySelector(`[data-review-form="${Number(button.dataset.refreshReview)}"]`);
    if (form) captureMember(form);
    return locked(() => refreshReview(Number(button.dataset.refreshReview)));
  }
  if (button.dataset.removeReview !== undefined) {state.queue.splice(Number(button.dataset.removeReview),1); state.reviewFocus = state.queue[0] ? queueId(state.queue[0]) : null; state.reviewPreview = null; state.reviewSelection++; persist(); render(); void loadReviewFocus(); return;}
  if (button.dataset.recover !== undefined) return locked(() => recover(Number(button.dataset.recover)));
  if (button.dataset.forget !== undefined) {state.pending.splice(Number(button.dataset.forget),1); persist(); render(); return;}
  if (button.dataset.rebaseTask !== undefined && state.detail) {
    const row = state.detail, draft = state.drafts[`task:${row.key}`];
    if (!draft) return;
    modal('核对当前来源与正文草稿', `<p>当前来源 Revision：${esc(row.revision)}</p><h3>当前正文</h3><pre>${esc(row.body || '')}</pre><h3>保留的草稿</h3><pre>${esc(draft.body)}</pre>`,
      async () => {draft.base_revision = row.revision; persist(); render();}, '将草稿基准改为当前来源');
    return;
  }
  if (button.dataset.action === 'reload') return reload();
  if (button.dataset.action === 'refresh-governance') return locked(() => refreshGovernance());
  if (button.dataset.action === 'load-gallery') return loadGalleryBatch();
  if (button.dataset.action === 'batch') {
    document.querySelectorAll('[data-review-form]').forEach(captureMember);
    return locked(() => prepareReview(state.queue));
  }
});
app.addEventListener('submit', event => {
  event.preventDefault();
  if (state.busy) return;
  if (event.target.id === 'task-form') {
    const body = event.target.querySelector('#task-body').value;
    return locked(() => prepareTask(body));
  }
  if (event.target.dataset.reviewForm !== undefined) {
    const item = captureMember(event.target);
    if (item) return locked(() => prepareReview([item]));
  }
});
app.addEventListener('change',event=>{
  if(event.target.id==='comparison-candidate'){state.comparison={key:state.selectedKey,id:event.target.value};render();void loadCandidatePreview(state.comparison.key,state.comparison.id);return;}
  if(event.target.id==='relation-document'){switchRelationView({relationNodeKey:event.target.value});return;}
  if (event.target.id==='relation-flow') {switchRelationView({relationFlowKey:event.target.value,relationNodeKey:null}); document.querySelector('#relation-flow')?.focus({preventScroll:true});}
});
app.addEventListener('change', event => {
  if(event.target.id==='relation-lens'){switchRelationView({relationLens:event.target.value==='impact'?'impact':'domains'});document.querySelector('#relation-lens')?.focus({preventScroll:true});return;}
  if(event.target.id==='relation-direction'){switchRelationView({relationDirection:event.target.value==='RIGHT'?'RIGHT':'DOWN'});document.querySelector('#relation-direction')?.focus({preventScroll:true});return;}
  if (event.target.id === 'project') return state.busy ? render() : chooseProject(event.target.value);
  if (event.target.dataset.filter) {state.filters[event.target.dataset.filter] = event.target.value; render(); return;}
  const form = event.target.closest('[data-review-form]');
  if (form) {
    captureMember(form);
    if(['conclusion','use_id'].includes(event.target.name))render();
  }
});
app.addEventListener('input', event => {
  if (event.target.id === 'search') {state.drafts.search = event.target.value; persist(); /* Keep focus while filtering. */
    let visible = 0;
    document.querySelectorAll('.source-item').forEach(item => {
      item.hidden = !item.textContent.toLowerCase().includes(event.target.value.toLowerCase());
      if (!item.hidden) visible++;
    });
    const count = document.querySelector('#source-count');
    if (count) count.textContent = `当前筛选 ${visible} / 已读取 ${state.records.length} 条`;
  }
  if (event.target.id === 'task-body' && state.detail) {
    const key = `task:${state.detail.key}`;
    state.drafts[key] = {body:event.target.value, base_revision:state.drafts[key]?.base_revision || state.detail.revision}; persist();
  }
  const form = event.target.closest('[data-review-form]'); if (form) captureMember(form);
});

app.addEventListener('error', event => {
  if (!event.target.matches?.('.asset-media img,.asset-media audio,.asset-media video,.review-preview img,.review-preview audio,.review-preview video')) return;
  const message = document.querySelector(event.target.closest('.review-preview')?'#review-media-error':'#media-error');
  if (message) message.textContent = '媒体加载失败或当前字节已变化。请刷新候选并重新核对。';
}, true);
const refreshCoordinator=createRefreshCoordinator({context,readVersions:bound=>api(`${boundBase(bound)}/revisions`),loadChanges:(bound,change)=>same(bound)?reload({automatic:true,expected:change.expected,affectedKeys:change.keys}):null,blocked:autoRefreshBlocked,status:refreshStatus});
window.addEventListener('focus',scheduleSourceCheck);
document.addEventListener('visibilitychange',()=>{if(!document.hidden)scheduleSourceCheck();});
app.addEventListener('focusout',()=>{if(refreshCoordinator.pending())scheduleSourceCheck();});
connect().catch(error => {app.innerHTML = `<main class="panel connect-error"><h1>无法连接工作台</h1><p class="error">${esc(issue(error))}</p><p class="notice">请使用本机面板启动方提供的连接链接，或检查现有会话。</p></main>`;});
