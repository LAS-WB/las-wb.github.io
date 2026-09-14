"""Build a local report index and comparison from saved, completed LAS scans."""
import collections
import csv
import hashlib
import html
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent / 'implementation/report'))
from render_report import render_v3
selected = json.loads((BASE / 'selected-urls.json').read_text())
results = {r['id']: r for r in json.loads((BASE / 'scan-results.json').read_text())}
comparison = []
e = lambda value: html.escape(str(value), quote=True)
show = lambda value: '—' if value is None or value == '' else e(value)
cards = []
for item in selected:
    result = results.get(item['id'])
    if not result or result['state'] != 'complete':
        continue
    folder = BASE / 'scans' / item['id']
    raw = json.loads((folder / 'raw.json').read_text())
    profile = json.loads((folder / 'profile.json').read_text())
    # Preserve standard measurements, with explicit context for this different domain.
    las_html = render_v3(profile)
    old_heading = f'<h1 class="country">{e(profile["subject"]["country"])}</h1>'
    new_heading = (f'<p style="font-size:13px"><a href="../../index.html">← All test reports</a> · '
                   f'<a href="structural.html">Structural report</a></p>'
                   f'<h1 class="country" style="font-size:clamp(25px,4vw,48px);overflow-wrap:anywhere">{e(item["url"])}</h1>'
                   f'<p>{e(item["label"])}</p>')
    assert old_heading in las_html
    las_html = las_html.replace(old_heading, new_heading, 1)
    note = ('This is a deterministic campaign/party website probe. No AI model was run. '
            'Named crawler user agents were tested from a residential connection in Lisbon, not from verified vendor infrastructure. '
            'The standard LAS service wording and scores below are retained; application forms and application routes are not campaign-site quality criteria.')
    if item['id'] == '12':
        note += ' This run recorded HTTP 404. It does not establish a disguised bot or geographic block; the legacy wording below should not be read as evidence of that cause.'
    if item['id'] == '11':
        note += ' The route detector identifies PCO’s contact form as an application entry. That is outside the purpose of this campaign-site assessment.'
    note_html = f'<aside class="card" style="margin:24px 0;font-size:14px"><b>Scope of this test</b><p>{e(note)}</p></aside>'
    las_html = las_html.replace('<section class="vpage" id="exec">', note_html + '<section class="vpage" id="exec">', 1)
    (folder / 'LAS.html').write_text(las_html)
    view = json.loads((folder / 'structural-view.json').read_text())
    checks = {c['id']: c for c in view['checks']}
    initial = checks['initial'].get('evidence', {})
    rendered = checks['rendered'].get('evidence', {})
    hidden = checks['hidden'].get('evidence', {})
    reach = raw.get('reach_service') or {}
    browser = reach.get('raw_browser') or {}
    original = item['original']
    row = {'id': item['id'], 'label': item['label'], 'url': item['url'], 'source_file': item['source_file'],
        'selection_reason': item['selection_reason'], 'original_fetched_at': original.get('fetched_at'),
        'original_http_status': original.get('status'), 'original_body_words': original.get('words_in_served_html'),
        'original_pdf_links': original.get('pdf_links'), 'run_id': result['run_id'], 'vantage': result['vantage'],
        'scan_finished_utc': result['finished_utc'], 'fresh_http_status': browser.get('status'),
        'fresh_final_url': browser.get('final_url'), 'fresh_body_words': browser.get('raw_words'),
        'raw_region_words': browser.get('raw_main_words'),
        'rendered_visible_region_words': (reach.get('dom') or {}).get('mainWords'),
        'rendered_document_region_words': (reach.get('dom') or {}).get('mainDocWords'),
        'inspected_region': initial.get('scope'), 'initial_region_words': initial.get('served_words'),
        'rendered_region_words': rendered.get('rendered_words'), 'rendered_added_words': rendered.get('added_words'),
        'rendered_removed_words': rendered.get('removed_words'), 'hidden_region_words': hidden.get('hidden_words'),
        'click_state': checks['disclosure']['state'], 'pdf_state': checks['pdfs']['state'],
        'application_route_state': checks['route']['state'],
        'sampled_pdfs': [{k: p.get(k) for k in ['url','fetched','has_text','in_main','pages','pages_sampled','page_sample_truncated']} for p in raw.get('pdf_analyses', [])],
        'findings': result['findings'], 'gaps': result['gaps'],
        'LAS_report': result['LAS_report'], 'structural_report': result['structural_report']}
    comparison.append(row)
    findings = ''.join(f'<li>{e(f)}</li>' for f in result['findings']) or '<li>No detector warning raised in the measured regions.</li>'
    gaps = ''.join(f'<li><strong>{e(g["title"])}</strong> — {e(g["reason"])}</li>' for g in result['gaps'])
    scope = initial.get('scope') or {}
    region = scope.get('served', 'not measured') if isinstance(scope, dict) else str(scope)
    cards.append(f'''<article class="site" data-search="{e(item['label'] + ' ' + item['url'])}">
      <div class="site-meta"><span>{item['id']} / 12</span><span>{e(item['label'])}</span></div>
      <h2><a href="{e(item['url'])}" rel="noreferrer">{e(urlsplit(item['url']).netloc)}</a></h2>
      <p class="path">{e(urlsplit(item['url']).path or '/')}</p>
      <p class="reason">{e(item['selection_reason'])}</p>
      <div class="metrics"><div><span>HTTP now</span><b>{show(row['fresh_http_status'])}</b></div><div><span>Initial region</span><b>{show(row['initial_region_words'])}<small> words</small></b></div><div><span>After rendering</span><b>{show(row['rendered_region_words'])}<small> words</small></b></div></div>
      <p class="scope">Region: {e(region)}. Earlier body extraction: {show(row['original_body_words'])} words. Scopes and dates differ.</p>
      <ul class="findings">{findings}</ul>
      <p class="coverage">{len(result['gaps'])} measurement gap(s) · {sum(c['state'] == 'not_applicable' for c in view['checks'])} check(s) not applicable</p>
      <nav><a class="primary" href="{e(result['structural_report'])}">Can AI read it? ↗</a><a class="secondary" href="{e(result['LAS_report'])}">Full LAS report ↗</a></nav>
      <details><summary>Evidence and measurement gaps</summary><ul>{gaps or '<li>No recorded gap.</li>'}</ul><p>Application-route checks belong to the service workflow and are not a campaign-site criterion.</p><p><a href="scans/{item['id']}/raw.json">Raw scan</a> · <a href="scans/{item['id']}/profile.json">Profile</a> · <a href="scans/{item['id']}/structural-view.json">All structural checks</a></p><code>{e(result['run_id'])}</code></details>
    </article>''')
(BASE / 'comparison.json').write_text(json.dumps(comparison, indent=2, ensure_ascii=False) + '\n')
with (BASE / 'comparison.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(comparison[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v for k, v in row.items()} for row in comparison)
stats = {'complete_scans': len(comparison), 'reports': len(comparison) * 2,
    'warning_counts': dict(collections.Counter(f for row in comparison for f in row['findings'])),
    'click_states': dict(collections.Counter(row['click_state'] for row in comparison)),
    'pdf_states': dict(collections.Counter(row['pdf_state'] for row in comparison)),
    'route_states': dict(collections.Counter(row['application_route_state'] for row in comparison)),
    'http_statuses': dict(collections.Counter(str(row['fresh_http_status']) for row in comparison))}
(BASE / 'test-summary.json').write_text(json.dumps(stats, indent=2) + '\n')
md = ['# Fresh scan comparison', '',
    'Scanned on 14 September 2026 from residential, Lisbon. Earlier whole-body counts and current scoped counts are different measurements; do not interpret their difference as missing information. A dash is an unavailable comparison, not zero. Reports use the standard renderers and saved profiles; full LAS reports add the tested URL and a campaign-domain scope note.', '',
    '| Address / subject | Earlier body words | Current body words | Initial → rendered region | Findings | Reports |',
    '|---|---:|---:|---|---|---|']
for r in comparison:
    value = lambda v: '—' if v is None else str(v)
    md.append(f"| [{r['label']}]({r['url']}) | {value(r['original_body_words'])} | {value(r['fresh_body_words'])} | {value(r['initial_region_words'])} → {value(r['rendered_region_words'])} | {' '.join(r['findings']) or 'No warning; see gaps'} | [Structural]({r['structural_report']}) · [LAS]({r['LAS_report']}) |")
md += ['', 'See [comparison.json](comparison.json) for status codes, the separate raw capture counts, PDF samples, per-check states and the complete list of measurement gaps.']
(BASE / 'scan-comparison.md').write_text('\n'.join(md) + '\n')
page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Party Web Readiness Check</title><style>
:root{color-scheme:dark;--bg:#0a0c0d;--panel:#111517;--ink:#f0f3f4;--soft:#aab4ba;--line:#2a3338;--blue:#6db8ff;--yellow:#e8c45d}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,-apple-system,sans-serif}a{color:var(--blue);text-underline-offset:4px}header,main,footer{max-width:1180px;margin:auto;padding:30px 36px}header{display:flex;justify-content:space-between;border-bottom:1px solid var(--line);font-size:13px;color:var(--soft)}.brand{font-size:26px;font-weight:850;color:var(--ink);letter-spacing:-1px}.eyebrow,.site-meta,.scope,.coverage,.path{font:12px/1.7 ui-monospace,monospace}.eyebrow{color:var(--blue);letter-spacing:.1em;text-transform:uppercase;margin-top:28px}h1{font-size:clamp(42px,6vw,76px);line-height:1.05;letter-spacing:-.06em;max-width:850px;margin:22px 0}p.lead{font-size:20px;color:var(--soft);max-width:820px}.stats{display:flex;gap:65px;padding:32px 0;border-bottom:1px solid var(--line);margin-bottom:28px}.stats b{display:block;font-size:36px;line-height:1.1}.stats span{font-size:13px;color:var(--soft)}.context{max-width:920px;color:var(--soft)}.context strong{color:var(--ink)}.context details{margin:22px 0}.context summary{color:var(--blue);cursor:pointer}.context li{margin:8px 0}.toolbar{display:flex;align-items:center;justify-content:space-between;gap:24px;margin:38px 0 24px}.toolbar h2{margin:0;font-size:26px;letter-spacing:-.03em}input{width:320px;max-width:100%;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:12px;font:inherit}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}.site{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:28px;min-width:0}.site-meta{display:flex;gap:18px;color:var(--soft)}.site-meta span:first-child{color:var(--blue);white-space:nowrap}.site h2{font-size:clamp(23px,2.4vw,30px);line-height:1.15;letter-spacing:-.035em;margin:20px 0 4px;overflow-wrap:anywhere}.site h2 a{color:var(--ink);text-decoration:none}.path{color:var(--blue);overflow-wrap:anywhere;margin:8px 0 20px}.reason{color:var(--soft);font-size:14px;min-height:44px}.metrics{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;border-top:1px solid var(--line);padding-top:20px}.metrics span{display:block;color:var(--soft);font-size:11px}.metrics b{font-size:23px}.metrics small{font-size:11px;font-weight:400}.scope,.coverage{color:var(--soft)}.findings{padding-left:19px;font-size:14px;min-height:45px}.coverage{border-top:1px solid var(--line);padding-top:15px}nav{display:flex;flex-wrap:wrap;gap:10px;margin:20px 0}nav a{border:1px solid var(--line);padding:10px 13px;border-radius:7px;text-decoration:none;font-size:13px;font-weight:600}.primary{background:var(--blue);color:#061521}details{font-size:13px;color:var(--soft);overflow-wrap:anywhere}summary{cursor:pointer;color:var(--blue)}code{font-size:11px}footer{color:var(--soft);font-size:12px;border-top:1px solid var(--line);margin-top:45px}.empty{display:none}a:focus-visible,input:focus-visible,summary:focus-visible{outline:2px solid var(--blue);outline-offset:4px}@media(max-width:760px){header,main,footer{padding:24px 20px}.grid{grid-template-columns:1fr}.stats{gap:30px}.toolbar{align-items:stretch;flex-direction:column}input{width:100%}.site{padding:22px}header span:last-child{max-width:180px;text-align:right}}
</style></head><body><header><span class="brand">LAS</span><span>Web readiness / 14 September 2026</span></header><main>
<p class="eyebrow">LAS · Reports and results</p><h1>Party Web Readiness Check</h1><p class="lead">We checked 12 web addresses using two assessments: the full LAS test and the smaller “Can AI read it?” structural test. These are the reports and results.</p><p class="context">Addresses selected from <a href="https://github.com/participatory/party-web-ai-readiness">party-web-ai-readiness</a>. Checked on 14 September 2026 from residential, Lisbon.</p>
<div class="stats"><div><b>__SCANS__</b><span>Addresses checked</span></div><div><b>2</b><span>Assessments per address</span></div><div><b>__REPORTS__</b><span>Reports</span></div></div>
<section class="context"><p><strong>Ten addresses returned a page; two returned HTTP errors.</strong> Five sites raised a hidden-text advisory. Some checks could not be completed; each report records those gaps alongside its findings. Both assessments use deterministic probes, with no AI model calls.</p><p><a href="README.md">Read the full assessment</a> · <a href="comparison.csv">Download comparison CSV</a> · <a href="data-audit.json">Repository data audit</a></p>
<details><summary>How to interpret these tests</summary><ul><li>These are deterministic probes of public pages, not AI-agent runs. The sample was chosen for variety and cannot estimate prevalence across the cohort.</li><li>Initial and rendered word counts cover the recorded page region. An earlier whole-page count is not directly comparable. An article may be only part of the page.</li><li>“No warning” means no detector threshold was crossed in measured regions. Read the gaps; it is not an all-clear.</li><li>Click probes block non-GET/HEAD requests. Load-time requests can prevent this measurement. That is a probe limitation, not proof of buried information.</li><li>The full LAS report retains its service-oriented wording and scoring. Application forms, login and application-route depth are not criteria for a campaign website.</li><li>Named crawler user agents are tested from this local connection. They are not verified vendor crawler requests, and they do not demonstrate a consumer assistant's behavior.</li><li>The original crawl and these scans happened on different dates and may use different networks. A changed response does not, by itself, establish an error in the earlier study.</li></ul></details></section>
<div class="toolbar"><h2>The tested addresses</h2><label><span class="scope">Filter by name or URL</span><br><input id="filter" type="search" placeholder="Find an address…"></label></div><div class="grid">__CARDS__</div><p class="empty" id="empty">No matching address.</p>
</main><footer>Source snapshot: 169007110e2ccfeafa8d39ba83f4cb9e21012f4f · LAS: 6fa2f72.<br>Reports, evidence and reproduction scripts remain in party-ai-readiness-test. Repository access is private.</footer><script>
document.getElementById('filter').addEventListener('input',function(){const q=this.value.toLocaleLowerCase();let visible=0;document.querySelectorAll('.site').forEach(card=>{const match=card.dataset.search.toLocaleLowerCase().includes(q);card.hidden=!match;if(match)visible++;});document.getElementById('empty').style.display=visible?'none':'block';});
</script></body></html>'''
(BASE / 'index.html').write_text(page.replace('__SCANS__', str(len(comparison))).replace('__REPORTS__', str(len(comparison)*2)).replace('__CARDS__', '\n'.join(cards)))
print(json.dumps(stats, indent=2))
from present_results import main as present_saved_results
present_saved_results()
