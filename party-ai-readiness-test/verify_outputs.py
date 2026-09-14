"""Verify saved artifacts and render representative local pages with Playwright."""
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parent
results = json.loads((BASE / 'scan-results.json').read_text())
assert len(results) == 12 and all(r['state'] == 'complete' for r in results)
assert len({r['run_id'] for r in results}) == 12
for r in results:
    p = BASE / r['profile']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == r['profile_sha256']
    for name in ['LAS_report', 'structural_report']:
        text = (BASE / r[name]).read_text()
        assert '<html' in text and '</html>' in text
        assert html.escape(r['url'], quote=True) in text
    view = json.loads((p.parent / 'structural-view.json').read_text())
    assert view['mock'] is False
    assert len(view['checks']) == 6
    assert view['provenance']['run_id'] == r['run_id']

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links += [v for k, v in attrs if k == 'href']

parser = Links(); parser.feed((BASE / 'index.html').read_text())
local_links = [u for u in parser.links if not urlsplit(u).scheme and not u.startswith('#')]
for u in local_links:
    assert (BASE / unquote(urlsplit(u).path)).exists(), u

qa = BASE / 'verification'; qa.mkdir(exist_ok=True)
checks = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for filename, width, height, shot in [
        ('index.html', 1440, 1100, 'index-desktop.png'),
        ('index.html', 390, 844, 'index-mobile.png'),
        ('scans/01/structural.html', 1280, 1000, 'structural-desktop.png'),
        ('scans/10/structural.html', 390, 844, 'structural-mobile.png'),
        ('scans/09/structural.html', 1280, 1000, 'unreadable-structural.png'),
        ('scans/04/LAS.html', 1440, 1000, 'las-desktop.png'),
    ]:
        page = browser.new_page(viewport={'width': width, 'height': height}, device_scale_factor=1)
        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.route('https://**/*', lambda route: route.abort())
        page.goto((BASE / filename).as_uri(), wait_until='load')
        overflow = page.evaluate('document.documentElement.scrollWidth > innerWidth')
        assert not overflow, (filename, width)
        assert not errors, errors
        if filename == 'index.html':
            assert page.locator('.site').count() == 12
            assert page.locator('nav a').count() == 24
            page.locator('#filter').fill('paula')
            assert page.locator('.site:visible').count() == 1
            page.locator('#filter').fill('unlikelymissingquery')
            assert page.locator('#empty').is_visible()
            page.locator('#filter').fill('')
        page.screenshot(path=str(qa / shot))
        checks.append({'file': filename, 'viewport': [width, height], 'horizontal_overflow': overflow, 'script_errors': errors, 'screenshot': str((qa / shot).relative_to(BASE))})
        page.close()
    browser.close()
summary = {'completed_runs': 12, 'verified_reports': 24, 'profile_hashes_match': True,
    'unique_run_ids': True, 'all_structural_reports_real': True,
    'local_index_links_checked': len(local_links), 'browser_checks': checks,
    'font_note': 'External requests blocked for offline layout checks; screenshots use local fallback fonts.'}
(qa / 'verification.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
