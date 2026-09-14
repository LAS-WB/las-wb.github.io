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


def describe(view, status):
    checks = {c['id']: c for c in view['checks']}
    initial = checks['initial']['evidence']
    hidden = checks['hidden']['evidence']
    measured = checks['initial']['state'] != 'not_measured'
    if all(c['state'] == 'not_measured' for c in view['checks']):
        lead = f'HTTP {status}: the page could not be read in this test.'
    elif measured:
        lead = (f"{initial['served_words']:,} words in the initial response; "
                f"{initial['rendered_words']:,} in the browser document after rendering.")
    else:
        lead = 'The initial and rendered text could not be compared: ' + checks['initial']['reason'] + '.'

    items = []
    for key in ['initial', 'rendered', 'hidden', 'disclosure', 'pdfs']:
        c = checks[key]
        if c['state'] == 'not_measured':
            continue
        observation = c['observation']
        if key == 'rendered' and measured:
            observation = (f"{initial['rendered_words']:,} words were extracted after rendering: "
                           f"{initial['matching_words']:,} matched the initial extraction, "
                           f"{initial['added_words']:,} were added and {initial['removed_words']:,} "
                           'initial words were not retained. This difference does not establish its cause.')
        if key == 'hidden':
            observation = (f"{hidden['document_words']:,} words in the inspected browser document: "
                           f"{hidden['visible_words']:,} visible and {hidden['hidden_words']:,} visually hidden.")
            mechanisms = hidden.get('mechanisms', {})
            if mechanisms:
                observation += ' Recorded mechanisms: ' + ', '.join(f'{k} ({v} words)' for k, v in mechanisms.items()) + '.'
            observation += ' Visually hidden text may still be available to a machine reader.'
        items.append(f'<li><b>{e(c["title"])}</b><p>{e(observation)}</p></li>')

    limitations = []
    scope = initial.get('scope', {})
    if scope:
        limitations.append('Text counts cover the selected region: initial ' + scope.get('served', 'unknown') +
                           ', rendered ' + scope.get('rendered', 'unknown') +
                           '. An article can be only part of the page. These are not whole-site totals; rendered document counts can include hidden text.')
    for c in view['checks']:
        if c['state'] == 'not_measured' and c['id'] != 'route':
            reason = c['reason']
            if 'non-read request' in reason:
                reason = ('the test blocked a request during page loading, before pressing any control. '
                          'The starting page was incomplete, so the test cannot establish what a click would reveal.')
            limitations.append(c['title'] + ': ' + reason)
    route = checks['route']
    route_text = route['reason'] if route['state'] == 'not_measured' else route['observation']
    limitations.append('Application-route test: ' + route_text +
                       ' This government-service check does not assess campaign information; a contact form is not evidence of a relevant application service.')
    limitations.append('These tests did not measure actual AI answers, information accuracy or completeness, search visibility, or whether the page answers a voter’s question.')
    return lead, items, limitations


def main():
    comparison = {r['id']: r for r in json.loads((BASE / 'comparison.json').read_text(encoding='utf-8'))}
    index_path = BASE / 'index.html'
    index = index_path.read_text(encoding='utf-8')
    for folder in sorted((BASE / 'scans').iterdir()):
        if not (folder / 'structural-view.json').exists():
            continue
        view = json.loads((folder / 'structural-view.json').read_text(encoding='utf-8'))
        lead, items, limitations = describe(view, comparison[folder.name]['fresh_http_status'])
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
        # Keep index summaries consistent with the report instead of saying "no warning".
        pattern = r'(<article class="site"[^>]*>.*?<span>' + folder.name + r' / 12</span>.*?<ul class="findings">).*?(</ul>)'
        index, count = re.subn(pattern, lambda m: m[1] + '<li>' + e(lead) + '</li>' + m[2], index, count=1, flags=re.S)
        assert count == 1, folder.name
    index = index.replace('Five sites raised a hidden-text advisory.', 'Reports show extracted text, changes after rendering, visually hidden words and PDF observations.')
    index = index.replace('“No warning” means no detector threshold was crossed in measured regions. Read the gaps; it is not an all-clear.', 'Read the measurements together with their scope and limitations. Available text does not establish that an AI can answer questions from it.')
    index_path.write_text(index, encoding='utf-8', newline='\n')
    manifest_path = BASE / 'artifact-manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    for entry in manifest['files']:
        data = (BASE / entry['path']).read_bytes()
        entry.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Updated 12 structural reports, index summaries and artifact hashes.')


if __name__ == '__main__':
    main()
