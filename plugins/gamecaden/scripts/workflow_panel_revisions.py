"""Content-based change probes for registered sources, without record parsing or caches."""
from __future__ import annotations
import os
from workflow_formats import WorkflowError, canonical, revision
from workflow_storage import STATE_NAME


def _sample(panel):
    guard=panel._project()  # Parses the registration mapping only, never document bodies.
    files={}; inventory=[]; diagnostics=[]
    mapping_revision=guard.observed.get(str(guard.workspace))
    def diagnostic(code,message,path,source):
        diagnostics.append({'code':code,'message':message,'ref':{'path':str(path)},'source_id':source})
    def add(path,source):
        path=guard.path(path)
        if not path.is_file():
            diagnostic('not_found','Registered source file is missing',path,source); return
        files.setdefault(str(path),set()).add(source)
    sources=panel.external_sources if panel.external_sources else guard.sources
    for source in sources:
        source_id=source['id']
        try:
            path=guard.path(source['path'],panel.root) if panel.external_sources else guard.source_path(source)
            kind='file' if panel.external_sources else source['kind']
            if not path.exists() and not panel.external_sources and guard.mapping is None:
                inventory.append({'id':source_id,'path':str(path),'kind':kind,'exists':False});continue
            inventory.append({'id':source_id,'path':str(path),'kind':kind,'exists':path.exists()})
            if kind=='file':add(path,source_id)
            elif not path.is_dir():diagnostic('not_found','Registered source collection is missing',path,source_id)
            else:
                def walk_error(exc):
                    diagnostic('read_failed','Registered collection could not be scanned',exc.filename or path,source_id)
                for directory,folders,names in os.walk(path,followlinks=False,onerror=walk_error):
                    folders[:]=[name for name in folders if name not in ('.git',STATE_NAME)
                                and not (guard.path(directory)/name).is_symlink()
                                and not (guard.path(directory)/name).is_junction()]
                    for name in sorted(names):
                        if os.path.splitext(name)[1].lower() in ('.md','.json','.yaml','.yml'):
                            add(guard.path(directory)/name,source_id)
        except (WorkflowError,OSError) as exc:
            diagnostic(getattr(exc,'code','read_failed'),str(exc) if isinstance(exc,WorkflowError) else 'Registered source could not be read',source.get('path',''),source_id)
    # Rule files are explicitly registered too. Runtime roots are deliberately not scanned.
    if not panel.external_sources:
        for source in (guard.mapping or {}).get('rule_sources',[]):
            try:add(guard.path(source['path'],guard.home),'rule:'+source['id'])
            except (WorkflowError,OSError) as exc:diagnostic(getattr(exc,'code','read_failed'),'Registered rule source could not be read',source['path'],source['id'])
    versions=[]
    for path,owners in sorted(files.items()):
        try:
            content=guard.read_bytes(guard.path(path))
            versions.append({'ref':{'path':path},'revision':revision(content),'source_ids':sorted(owners)})
        except (WorkflowError,OSError) as exc:
            diagnostic(getattr(exc,'code','read_failed'),str(exc) if isinstance(exc,WorkflowError) else 'Registered source could not be read',path,','.join(sorted(owners)))
    # The mapping itself is also observed after all source bytes have been read.
    if guard.workspace.exists():
        try:
            guard.read_bytes(guard.workspace)
            if mapping_revision is None:diagnostic('revision_conflict','Source mapping appeared during reading',guard.workspace,None)
        except (WorkflowError,OSError) as exc:diagnostic(getattr(exc,'code','read_failed'),'Source mapping changed or could not be read',guard.workspace,None)
    elif mapping_revision is not None:
        diagnostic('revision_conflict','Source mapping disappeared during reading',guard.workspace,None)
    binding={'root':str(panel.root),'project_id':panel.project_id,'name':panel.name,
             'workspace':str(guard.workspace),'external_sources':panel.external_sources}
    material={'binding':binding,'mapping_revision':mapping_revision,'inventory':inventory,'source_revisions':versions}
    return material,diagnostics


def source_revisions(panel):
    """Two independent byte-hash passes catch observed membership/content races.

    No mtime trust or persistent cache. This is an observation, not a filesystem
    transaction: changes after the final pass are seen by the next probe/read.
    """
    first,diagnostics=_sample(panel)
    second,other=_sample(panel)
    diagnostics+=other
    if first!=second:
        diagnostics.append({'code':'revision_conflict','message':'Registered sources changed during the version check'})
    # Keep diagnostics legible when both passes observed the same missing file.
    diagnostics=list({canonical(d):d for d in diagnostics}.values())
    return {'digest':revision(canonical(second).encode('utf-8')) if not diagnostics else None,
            'complete':not diagnostics,'mapping_revision':second['mapping_revision'],
            'source_revisions':second['source_revisions'],'diagnostics':diagnostics}
