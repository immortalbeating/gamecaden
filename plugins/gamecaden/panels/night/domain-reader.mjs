import {responsibility,sourceRange} from './relation-layout.mjs';

export function domainTree(data){
  const records=data.nodes.filter(node=>node.record_key&&!node.source_key),lookup=new Map(records.map(node=>[node.key,node])),children=new Map();
  for(const node of records){const parent=lookup.get(node.navigation_parent_key);if(parent&&parent.external===node.external){if(!children.has(parent.key))children.set(parent.key,[]);children.get(parent.key).push(node);}}
  const roots=records.filter(node=>!lookup.has(node.navigation_parent_key)||lookup.get(node.navigation_parent_key).external!==node.external);
  return {records,lookup,children,inside:roots.filter(node=>!node.external),outside:roots.filter(node=>node.external)};
}
export function focusSourceData(data,selectedKey,only=true){
  if(!only)return data;
  const lookup=new Map(data.nodes.map(node=>[node.key,node])),selected=lookup.get(selectedKey);
  if(!selected)return data;
  const keys=new Set([selectedKey]);
  for(const edge of data.edges)if(edge.from===selectedKey||edge.to===selectedKey){keys.add(edge.from);keys.add(edge.to);}
  if(lookup.has(selected.navigation_parent_key))keys.add(selected.navigation_parent_key);
  for(const node of data.nodes)if(node.navigation_parent_key===selectedKey)keys.add(node.key);
  if(lookup.has(selected.source_key))keys.add(selected.source_key);
  return {...data,nodes:data.nodes.filter(node=>keys.has(node.key)),edges:data.edges.filter(edge=>keys.has(edge.from)&&keys.has(edge.to)),groups:data.groups.filter(group=>data.nodes.some(node=>keys.has(node.key)&&node.group===group))};
}
export function chapterText(body,fragment){
  if(!fragment)return {text:body,located:true,excerpt:false};
  const range=sourceRange(body,fragment);
  if(!range)return {text:'',located:false,excerpt:false};
  const line=body.slice(range.start,range.end),heading=/^\s*(#{1,6})\s/.exec(line);
  if(!heading){const lines=body.split('\n'),index=body.slice(0,range.start).split('\n').length-1;return {text:lines.slice(Math.max(0,index-3),index+10).join('\n'),located:true,excerpt:true};}
  const lines=body.slice(range.end).split('\n'),level=heading[1].length;let fence=null,end=lines.length;
  for(let i=0;i<lines.length;i++){
    const clean=lines[i].trim();
    if(fence){if(new RegExp('^'+fence[0]+'{'+fence.length+',}\\s*$').test(clean))fence=null;continue;}
    const opening=/^(`{3,}|~{3,})/.exec(clean);if(opening){fence=opening[1];continue;}
    const next=/^(#{1,6})\s/.exec(clean);
    if(clean==='<!-- workflow:governance -->'||next&&next[1].length<=level){end=i;break;}
  }
  return {text:line+'\n'+lines.slice(0,end).join('\n').trim(),located:true,excerpt:false,matches:range.matches};
}
function readable(text,esc){
  const blocks=[];let paragraph=[],code=[],fence=null;
  const flush=()=>{if(paragraph.length){blocks.push(`<p>${paragraph.map(esc).join('<br>')}</p>`);paragraph=[];}};
  for(const line of text.split('\n')){
    const clean=line.trim(),opening=/^(`{3,}|~{3,})/.exec(clean);
    if(fence){if(opening&&opening[1][0]===fence[0]&&opening[1].length>=fence.length){blocks.push(`<pre>${esc(code.join('\n'))}</pre>`);code=[];fence=null;}else code.push(line);continue;}
    if(opening){flush();fence=opening[1];continue;}
    const heading=/^#{1,6}\s+(.+)$/.exec(clean);
    if(heading){flush();blocks.push(`<h4>${esc(heading[1])}</h4>`);}else if(!clean)flush();else paragraph.push(line);
  }
  flush();if(code.length)blocks.push(`<pre>${esc(code.join('\n'))}</pre>`);return blocks.join('')||'<p class="relation-note">此章节暂无正文。</p>';
}
export function renderDomainReader(data,lookup,selectedKey,ui,{esc,sourceButton,extraDetails}){
  const tree=domainTree(data),selected=lookup.get(selectedKey),owner=lookup.get(selected?.source_key)||selected,reader=ui.reader||{};
  function branch(node,seen=new Set()){
    if(seen.has(node.key))return '';const next=new Set([...seen,node.key]),children=tree.children.get(node.key)||[],open=ui.expanded?.has(node.key);
    return `<li><div class="reader-tree-row"><button id="reader-node-${esc(encodeURIComponent(node.key))}" data-reader-node="${esc(node.key)}" aria-current="${owner?.key===node.key}"><strong>${esc(node.title)}</strong><span>${esc(responsibility(node))}</span></button>${children.length?`<button class="reader-tree-fold" id="reader-fold-${esc(encodeURIComponent(node.key))}" data-reader-toggle="${esc(node.key)}" aria-expanded="${Boolean(open)}" aria-label="${open?'收起':'展开'} ${esc(node.title)}">${open?'收起':'展开'}</button>`:''}</div>${children.length?`<ul ${open?'':'hidden'}>${children.map(child=>branch(child,next)).join('')}</ul>`:''}</li>`;
  }
  const navigation=`<nav class="domain-doc-tree" aria-label="领域文档树" data-reading-scroll="domain-tree"><h3>领域文档</h3><ul>${tree.inside.map(node=>branch(node)).join('')}</ul>${tree.outside.length?`<details class="reader-external" data-reading-detail="reader-external"><summary>外部关联 · ${tree.outside.length}</summary><ul>${tree.outside.map(node=>branch(node)).join('')}</ul></details>`:''}</nav>`;
  const chapterCounts=new Map(),chapters=(owner?.headings||[]).filter(heading=>heading.level>1);
  const record=reader.nodeKey===selectedKey?reader.record:null,fragment=reader.fragment||'';
  const excerpt=record?chapterText(record.body||'',fragment):null;
  const content=reader.loading?'<p class="relation-note" role="status">正在读取原文…</p>':reader.error?`<p class="warning">${esc(reader.error)}</p><button class="quiet" id="reader-retry" data-reader-retry>重读此文档</button>`:!record?'<p class="relation-note">选择文档后读取原文。</p>':!excerpt.located?`<p class="warning">原条目未找到：${esc(fragment)}。请核对当前来源。</p>`:excerpt.excerpt?`<p class="relation-note">原条目位置 · 节选</p><pre>${esc(excerpt.text)}</pre>`:readable(excerpt.text,esc);
  const article=`<article class="domain-document-reader" aria-label="文档阅读区" data-reading-scroll="domain-reader" data-reading-key="${esc(selectedKey)}:${esc(fragment)}"><header><span class="reader-location">${esc(ui.domainFocus)} / ${esc(owner?.title||'未定位')}</span><h3>${esc(selected?.title||'选择文档')}</h3><p class="reader-duty">${esc(selected?responsibility(selected):'')}</p><div class="reader-source-actions">${sourceButton({...selected,ref:{...selected?.ref,fragment}},lookup,esc,'打开原文位置')}<button class="quiet" data-relation-domain-view="graph">在焦点关系图查看</button></div></header>${chapters.length?`<nav class="reader-chapters" aria-label="原文章节">${chapters.map(heading=>{const ordinal=chapterCounts.get(heading.fragment)||0;chapterCounts.set(heading.fragment,ordinal+1);return `<button id="reader-chapter-${esc(encodeURIComponent(selectedKey))}-${esc(encodeURIComponent(heading.fragment))}-${ordinal}" data-reader-chapter="${esc(heading.fragment)}" aria-current="${heading.fragment===fragment}">${esc(heading.text)}</button>`;}).join('')}<button id="reader-fulltext" data-reader-chapter="" aria-current="${!fragment}">全文</button></nav>`:''}<section class="reader-body">${content}</section>${record?`<details data-reading-detail="reader-original"><summary>完整原文与版本</summary><p class="reader-path">${esc(record.path)} · ${esc(record.revision)}</p><pre>${esc(record.body||'')}</pre></details>`:''}${extraDetails||''}</article>`;
  return `<div class="domain-reader-layout" data-domain-ready="true">${navigation}${article}</div>`;
}
