"""Present saved structural measurements without relying on warning thresholds.

Run after rendering reports. Uses saved evidence only; does not rescan sites.
"""
import hashlib
import html
import json
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent
e = lambda value: html.escape(str(value), quote=True)


def describe(view, narrative):
    checks = {c['id']: c for c in view['checks']}
    items = [f'<li><b>What this means</b><p>{e(narrative["meaning"])}</p></li>',
             f'<li><b>What a follow-up check needs to establish</b><p>{e(narrative["next"])}</p></li>']
    limitations = []
    scope = checks['initial']['evidence'].get('scope', {}).get('served')
    if scope == 'article':
        limitations.append('The scanner selected an article section, which may be only a small part of the page. The results do not cover the full website.')
    elif scope:
        limitations.append('The scanner inspected a selected content region and some linked material. It did not audit every page of the website.')
    click = checks['disclosure']
    if click['state'] == 'not_measured' and 'non-read request' in click['reason']:
        limitations.append('We could not check whether buttons reveal more information. The test blocked a request while the page was loading and stopped that check before clicking anything. This is a limitation of the test, not evidence that the site hides information behind clicks.')
    elif click['state'] == 'not_applicable':
        limitations.append('The test found no eligible control to press in the inspected area. This does not rule out interactive content elsewhere on the page.')
    if not all(c['state'] == 'not_measured' for c in view['checks']):
        limitations.append('The test did not establish whether the captured text contains complete, accurate answers about the candidate. Visual hiding does not by itself prevent a machine from reading the page code.')
    limitations.append('No AI assistant was asked questions in these runs. Search visibility and answer accuracy were not tested. The separate government-service application-route check is not a measure of campaign-site quality.')
    return narrative['lead'], items, limitations


def write_analysis(narratives, comparison):
    intro = '''# What the twelve website checks tell us

These checks found examples of accessible text, differences between ways of reading a page, and visits that could not be assessed. They did not establish whether an AI assistant can answer a voter's questions. This is an interpretation of the saved 14 September 2026 scans from Lisbon, not a new scan or a ranking of websites.

The clearest text-access result is the PCO article: the inspected main text was already in the server response and remained available after browser rendering. Other pages also supplied text without JavaScript, but the evidence is less conclusive about coverage. For Eduardo Riedel, Time Barra and NOVO, the scanner selected an article that may cover only part of the page. A smaller extraction after rendering does not establish that the website deleted information or that AI cannot read it.

Seven captures contained visually hidden words; five crossed the detector's warning threshold. The other two still matter: Time Barra's entire small captured article was transparent, while PCO's hidden sample consisted of sharing and comment-interface labels. Warning counts are therefore a poor summary of what was found. Hidden text can remain available to a reader of the page code, and this test does not determine whether scrolling, animation or another interaction makes it visible later.

Two addresses could not be assessed: Paula Belmonte returned an access refusal (403), and Riedel's communities address returned a not-found error (404). These are results for those requests, not evidence that all AI systems are blocked or that a whole website is unavailable. Acir Gurgacz responded but yielded no browser content words in the selected region. Orleans Brandao yielded browser text, but the detector declined the before/after comparison because the browser URL ended in #/.

Nine click checks stopped because the guarded test blocked a request during loading; two more could not run on the error pages. The remaining check found no eligible control. None establishes whether voters can uncover useful information by clicking. Three PDF samples across the full scans contained extractable text, but only three pages per file were sampled. The structural report's in-region PDF example is Flavio Bolsonaro's plan: three of 76 pages inspected.

The next useful step is to inspect the actual captured passages, confirm that the correct page regions and linked documents were covered, and test specific questions against those passages. The source study's candidate inventory and declared-address categories remain a baseline; this purposive twelve-address sample does not revise the cohort percentages or measure prevalence. Its scans also cannot establish the cause of differences from earlier visits. The saved audit of the source study reported an uncoded model pilot; these website probes do not complete that evaluation.

## Each address, in plain language
'''
    parts = [intro]
    rows = ['# Website checks: plain-language comparison', '',
            'These are interpretations of saved scans, not new measurements. The numerical evidence remains in [comparison.json](comparison.json). Read the [overall analysis](analysis.md) for shared limitations.', '',
            '| Address | What the test establishes |', '|---|---|']
    for key, narrative in narratives.items():
        label = comparison[key]['label']
        url = f'https://las-wb.github.io/party-ai-readiness-test/scans/{key}/structural.html'
        parts += [f'### {label}', '', narrative['lead'], '', narrative['meaning'], '',
                  '**Follow-up:** ' + narrative['next'], '', f'[Report and saved evidence]({url})', '']
        rows.append(f'| [{label}]({url}) | {narrative["lead"]} |')
    (BASE / 'analysis.md').write_text('\n'.join(parts), encoding='utf-8', newline='\n')
    (BASE / 'scan-comparison.md').write_text('\n'.join(rows) + '\n', encoding='utf-8', newline='\n')


def main():
    narratives = json.loads((BASE / 'interpretations.json').read_text(encoding='utf-8'))
    comparison = {r['id']: r for r in json.loads((BASE / 'comparison.json').read_text(encoding='utf-8'))}
    index_path = BASE / 'index.html'
    index = index_path.read_text(encoding='utf-8')
    for folder in sorted((BASE / 'scans').iterdir()):
        if not (folder / 'structural-view.json').exists():
            continue
        view = json.loads((folder / 'structural-view.json').read_text(encoding='utf-8'))
        lead, items, limitations = describe(view, narratives[folder.name])
        body = ('<section class="sr-observations" aria-label="Test results"><h2>What the tests found</h2>'
                f'<p class="sr-intro">{e(lead)}</p><ul>{"".join(items)}</ul></section>'
                '<section class="sr-gaps"><h2>What these tests could not establish</h2>' +
                ''.join(f'<p>{e(t)}</p>' for t in limitations) + '</section>'
                '<p class="sr-scope"><a href="../../index.html">All 12 tested addresses</a> · '
                '<a href="structural-view.json">Saved measurement evidence</a></p>')
        path = folder / 'structural.html'
        source = path.read_text(encoding='utf-8')
        start = source.index('</header>', source.index('<header class="sr-hero"')) + len('</header>')
        end = source.index('<details class="sr-details">', start)
        source = source[:start] + body + source[end:]
        path.write_text(source, encoding='utf-8', newline='\n')
        # The full LAS report carries the same interpretation above its legacy scores.
        full_path = folder / 'LAS.html'
        full = full_path.read_text(encoding='utf-8')
        full = re.sub(r'<aside data-party-interpretation="true">.*?</aside>', '', full, flags=re.S)
        interpretation = (f'<aside data-party-interpretation="true"><h2>What this run tells us</h2>'
                          f'<p>{e(lead)}</p><p>{e(narratives[folder.name]["meaning"])}</p>'
                          '<p>The service scores below do not measure campaign information quality or AI answer accuracy. '
                          '<a href="structural.html">Read the interpretation and test limitations</a>.</p></aside>')
        assert '<section class="vpage" id="exec">' in full
        full = full.replace('<section class="vpage" id="exec">', interpretation + '<section class="vpage" id="exec">', 1)
        full_path.write_text(full, encoding='utf-8', newline='\n')
        # Keep index summaries consistent with the report instead of saying "no warning".
        pattern = r'(<article class="site"[^>]*>.*?<span>' + folder.name + r' / 12</span>.*?<ul class="findings">).*?(</ul>)'
        index, count = re.subn(pattern, lambda m: m[1] + '<li>' + e(lead) + '</li>' + m[2], index, count=1, flags=re.S)
        assert count == 1, folder.name
    index = index.replace('Five sites raised a hidden-text advisory.', 'Reports show extracted text, changes after rendering, visually hidden words and PDF observations.')
    index = index.replace('“No warning” means no detector threshold was crossed in measured regions. Read the gaps; it is not an all-clear.', 'Read the measurements together with their scope and limitations. Available text does not establish that an AI can answer questions from it.')
    index = index.replace('<a href="README.md">Read the full assessment</a>', '<a href="analysis.md">What the results mean</a> · <a href="README.md">Read the source-study assessment</a>')
    # Keep the evidence verdict before the report catalogue, with methods after it.
    start = index.index('<p class="eyebrow">', index.index('<main>'))
    end = index.index('<div class="toolbar"', start)
    index = index[:start] + (BASE / 'index-summary.html').read_text(encoding='utf-8') + '\n' + index[end:]
    index = index.replace('<div class="toolbar"><h2>', '<div class="toolbar" id="tested-addresses"><h2>')
    index = re.sub(r'<section class="methods context".*?</section>\s*', '', index, flags=re.S)
    index = index.replace('</main>', (BASE / 'index-methods.html').read_text(encoding='utf-8') + '\n</main>')
    index = re.sub(r'/\* verdict styles \*/.*?/\* end verdict styles \*/', '', index, flags=re.S)
    styles = '''/* verdict styles */
h1{font-size:clamp(32px,5vw,54px);margin:12px 0 28px}
.verdict{max-width:960px}.verdict>.eyebrow{margin:0 0 12px;color:var(--yellow)}
.verdict h2{font-size:clamp(27px,3.5vw,40px);line-height:1.18;letter-spacing:-.025em;margin:0 0 18px}
.verdict-lead{font-size:19px;line-height:1.65;max-width:850px;color:var(--ink)}
.verdict-points{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px;margin:28px 0}
.verdict-points article{border-top:1px solid var(--line);padding:22px 0;min-width:0}
.verdict h3{font-size:20px;line-height:1.35;margin:0 0 12px}.verdict-points p{color:var(--soft);font-size:15px}
.verdict strong{color:var(--ink)}.verdict-scope{font-size:12px;color:var(--soft)}
.verdict-jumps{display:flex;flex-wrap:wrap;gap:12px 28px;padding:16px 0;border-bottom:1px solid var(--line)}
.methods{margin:50px 0 0;padding:28px 0;border-top:1px solid var(--line)}.methods h2{color:var(--ink)}
#tested-addresses,#how-checked{scroll-margin-top:24px}
@media(max-width:760px){.verdict-points{grid-template-columns:1fr;gap:0}.verdict-lead{font-size:17px}}
/* end verdict styles */'''
    index = index.replace('</style>', styles + '</style>', 1)
    index_path.write_text(index, encoding='utf-8', newline='\n')
    write_analysis(narratives, comparison)
    manifest_path = BASE / 'artifact-manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    for entry in manifest['files']:
        # Published text uses Git's LF form, even in a Windows CRLF checkout.
        data = (BASE / entry['path']).read_bytes().replace(b'\r\n', b'\n')
        entry.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Updated 12 structural reports, index summaries and artifact hashes.')


if __name__ == '__main__':
    main()
