"""Read-only, independent record audit of the downloaded repository snapshot."""
import collections as C
import csv
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parent
ROOT = BASE / 'repository'
out = {'scope': 'All CSV/JSON/JSONL records parsed structurally; response facts were not adjudicated.'}
tables = {}
out['csv'] = {}
for path in sorted(ROOT.rglob('*.csv')):
    name = str(path.relative_to(ROOT))
    rows = list(csv.DictReader(path.open(encoding='utf-8-sig')))
    tables[name] = rows
    out['csv'][name] = {'rows': len(rows), 'fields': list(rows[0]) if rows else [],
        'nonblank_by_field': {k: sum(bool(r.get(k, '').strip()) for r in rows) for k in rows[0]} if rows else {}}
out['json'] = {}
for path in sorted(ROOT.rglob('*.json')):
    name = str(path.relative_to(ROOT))
    raw = path.read_bytes()
    record = {'sha256': hashlib.sha256(raw).hexdigest()}
    try:
        value = json.loads(raw.decode('utf-8-sig'))
        record['valid_utf8_json'] = True
    except (UnicodeError, ValueError) as exc:
        record['valid_utf8_json'] = False
        record['error'] = str(exc)
        recovered = raw.decode('utf-8-sig', errors='replace')
        record['replacement_characters'] = recovered.count('\ufffd')
        try:
            value = json.loads(recovered)
            record['parseable_after_lossy_decode'] = True
        except ValueError:
            value = None
    record['type'] = type(value).__name__
    record['top_level_length'] = len(value) if isinstance(value, (dict, list)) else None
    out['json'][name] = record
out['jsonl'] = {}
for path in sorted(ROOT.rglob('*.jsonl')):
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
    out['jsonl'][str(path.relative_to(ROOT))] = {'rows': len(rows)}
    if path.name == 'gate5-pilot-responses.jsonl':
        counts = C.Counter((r['request_id'], r['model_id'], r['repetition']) for r in rows)
        reqs = tables['data/prompts/derived/pilot-request-matrix.csv']
        models = sorted({r['model_id'] for r in rows})
        expected = {(r['request_id'], model, rep) for r in reqs for model in models for rep in [1, 2]}
        out['current_api_pilot'] = {
            'rows': len(rows), 'unique_cells': len(counts), 'expected_cells': len(expected),
            'missing_cells': sorted(expected - set(counts)), 'unexpected_cells': sorted(set(counts) - expected),
            'duplicate_cells': [list(k) for k, v in counts.items() if v != 1],
            'models': dict(C.Counter(r['model_id'] for r in rows)),
            'candidates': len({r['sq_candidato'] for r in rows}), 'prompts': len({r['prompt_id'] for r in rows}),
            'coding_status': dict(C.Counter(r.get('coding_status') for r in rows)),
            'finish_reason': dict(C.Counter(r.get('finish_reason') for r in rows)),
            'empty_responses': sum(not (r.get('response_text') or '').strip() for r in rows),
            'recorded_errors': sum(bool(r.get('api_error')) for r in rows),
            'parameters': {m: list({json.dumps(r['parameters'], sort_keys=True) for r in rows if r['model_id'] == m}) for m in models},
            'dates_utc': [min(r['sent_at_utc'] for r in rows), max(r['sent_at_utc'] for r in rows)],
        }
bands = tables['data/gate6/candidate-bands.csv']
flag = lambda r, k: r.get(k) == 'True'
def category(r):
    if flag(r, 'own_readable'):
        return 'own_site_structured' if flag(r, 'has_sitemap') or flag(r, 'has_jsonld') else 'own_site_plain'
    if flag(r, 'candidacy_page'): return 'party_page_only'
    if flag(r, 'measured_live'): return 'live_but_nothing_readable'
    if r['reach_state'] == 'challenge': return 'bot_check_stopped_reader'
    if r['reach_state'] in {'domain_nonexistent', 'dns_resolution_error', 'http_error', 'unreachable', 'domain_parked'}: return 'address_error_at_visit'
    if r['party'] == 'PCB': return 'bot_check_stopped_reader'
    return 'no_address_declared'
out['candidate_categories'] = {
    'rows': len(bands), 'unique_ids': len({r['sq_candidato'] for r in bands}),
    'counts': dict(C.Counter(r['category'] for r in bands)),
    'independent_category_rule_mismatches': [r['sq_candidato'] for r in bands if category(r) != r['category']],
    'offices': dict(C.Counter(r['office'] for r in bands)),
    'parties': len({r['party'] for r in bands}),
    'qualifying_llms_txt': sum(flag(r, 'has_llms_txt') for r in bands),
    'robots_ai_blocks': sum(flag(r, 'robots_blocks_ai_crawlers') for r in bands),
}
out['candidate_join_ids'] = {}
ids = {r['sq_candidato'] for r in bands}
for name, rows in tables.items():
    if len(rows) == 527 and 'sq_candidato' in rows[0]:
        other = [r['sq_candidato'] for r in rows]
        out['candidate_join_ids'][name] = {'duplicates': len(other) - len(set(other)), 'missing': sorted(ids - set(other)), 'extra': sorted(set(other) - ids)}
out['sweeps'] = {}
for name in ['data/sweep/sweep-results.csv', 'data/sweep/sweep-new-2026-09-03.csv', 'data/sweep/party-sweep.csv']:
    rows = tables[name]
    evidence = {}
    for key in ['evidence_page', 'evidence_robots']:
        refs = [r[key] for r in rows if r.get(key)]
        evidence[key] = {'references': len(refs), 'present_in_snapshot': sum((ROOT / p).exists() for p in refs), 'unique_references': len(set(refs))}
    out['sweeps'][name] = {'rows': len(rows), 'unique_urls': len({r['url'] for r in rows}),
        'unique_hosts': len({urlsplit(r['url']).hostname for r in rows}),
        'http_status': dict(C.Counter(r['status'] or 'unrecorded' for r in rows)), 'evidence': evidence,
        'dates': [min(r['fetched_at'] for r in rows), max(r['fetched_at'] for r in rows)]}
out['initial_supplement_url_overlap'] = sorted({r['url'] for r in tables['data/sweep/sweep-results.csv']} & {r['url'] for r in tables['data/sweep/sweep-new-2026-09-03.csv']})
out['party_text_artifacts'] = len(list((ROOT / 'data/sweep/party-pages').glob('*.txt')))
out['threshold_sensitivity'] = tables['data/gate6/band-sensitivity.csv']
out['legacy_coverage_flag_conflicts'] = sum(r['coverage_tier'] != 'candidacy' and flag(r, 'counts_as_coverage') for r in tables['data/party-coverage-tiered.csv'])
(BASE / 'data-audit.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({k: out[k] for k in ['candidate_categories', 'current_api_pilot', 'sweeps', 'initial_supplement_url_overlap', 'party_text_artifacts', 'threshold_sensitivity', 'legacy_coverage_flag_conflicts']}, indent=2, ensure_ascii=False))
