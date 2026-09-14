"""Run the unchanged LAS scanner on the fixed 12-URL sample. No AI model calls."""
import concurrent.futures
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sys
import time
import traceback
from datetime import datetime,timezone

BASE=Path(__file__).resolve().parent
LAS=BASE.parent
sys.path[:0]=[str(LAS/'implementation/service'),str(LAS/'implementation/report'),str(LAS/'implementation/pillars/deterministic-scanner')]
VANTAGE='residential, Lisbon'

def scan_one(row):
    import las_scanner
    from app.scanjob import check_public
    from render_report import render_v3,render_structural
    from structural_report import build_structural_view
    folder=BASE/'scans'/row['id']
    folder.mkdir(parents=True,exist_ok=True)
    result={'id':row['id'],'label':row['label'],'url':row['url'],'vantage':VANTAGE,'started_utc':datetime.now(timezone.utc).isoformat()}
    try:
        check_public(row['url'])
        # LAS run ids use epoch seconds. Space concurrent starts without changing the scanner.
        with (BASE/'scan-start.lock').open('a+') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            time.sleep(2)
            start=time.time()
            # Release only after the worker is about to enter the scanner; next worker waits 2s.
        raw,profile=las_scanner.scan(country=row['label'],homepage=row['url'],service=row['url'],vantage='residential',pillars=['D','L','O','N','T'])
        raw['vantage']=VANTAGE
        profile['subject']['vantage']=VANTAGE
        profile['provenance']['vantage']=VANTAGE
        raw_path=folder/'raw.json'; profile_path=folder/'profile.json'
        raw_path.write_text(json.dumps(raw,indent=2,ensure_ascii=False))
        profile_path.write_text(json.dumps(profile,indent=2,ensure_ascii=False))
        (folder/'LAS.html').write_text(render_v3(profile))
        (folder/'structural.html').write_text(render_structural(profile))
        view=build_structural_view(profile)
        (folder/'structural-view.json').write_text(json.dumps(view,indent=2,ensure_ascii=False))
        result.update(state='complete',run_id=profile['provenance']['run_id'],elapsed_seconds=round(time.time()-start),
                      profile_sha256=hashlib.sha256(profile_path.read_bytes()).hexdigest(),
                      findings=[f['title'] for f in view['findings']],gaps=view['gaps'],
                      profile=str(profile_path.relative_to(BASE)),LAS_report=str((folder/'LAS.html').relative_to(BASE)),
                      structural_report=str((folder/'structural.html').relative_to(BASE)))
    except Exception as exc:
        result.update(state='failed',error=f'{type(exc).__name__}: {exc}')
        (folder/'error.txt').write_text(traceback.format_exc())
    result['finished_utc']=datetime.now(timezone.utc).isoformat()
    (folder/'result.json').write_text(json.dumps(result,indent=2,ensure_ascii=False))
    return result

if __name__=='__main__':
    rows=json.loads((BASE/'selected-urls.json').read_text())
    assert len(rows)==12
    results=[]
    pending=[]
    for row in rows:
        existing=BASE/'scans'/row['id']/'result.json'
        if existing.exists():
            saved=json.loads(existing.read_text())
            if saved.get('state')=='complete':
                results.append(saved);continue
        pending.append(row)
    print(json.dumps({'started_utc':datetime.now(timezone.utc).isoformat(),'urls':len(pending),'workers':2,'vantage':VANTAGE}),flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        futures={executor.submit(scan_one,row):row for row in pending}
        for future in concurrent.futures.as_completed(futures):
            result=future.result();results.append(result)
            (BASE/'scan-results.json').write_text(json.dumps(sorted(results,key=lambda r:r['id']),indent=2,ensure_ascii=False))
            print(json.dumps(result,ensure_ascii=False),flush=True)
    run_ids=[r['run_id'] for r in results if r['state']=='complete']
    assert len(run_ids)==len(set(run_ids)), 'Duplicate scanner run ids'
    print('FINISHED',len(results),'complete',sum(r['state']=='complete' for r in results),flush=True)
