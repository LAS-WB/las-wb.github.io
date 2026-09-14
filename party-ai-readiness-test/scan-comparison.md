# Website checks: plain-language comparison

These are interpretations of saved scans, not new measurements. The numerical evidence remains in [comparison.json](comparison.json). Read the [overall analysis](analysis.md) for shared limitations.

| Address | What the test establishes |
|---|---|
| [Renan Santos](https://las-wb.github.io/party-ai-readiness-test/scans/01/structural.html) | Some campaign text was available without JavaScript, but the browser exposed a different mix of text and left part of it visually hidden. |
| [Eduardo Riedel](https://las-wb.github.io/party-ai-readiness-test/scans/02/structural.html) | We could extract some text without running the page’s JavaScript, but this test does not establish how much useful candidate information is accessible. |
| [Time Barra / Eder Mauro](https://las-wb.github.io/party-ai-readiness-test/scans/03/structural.html) | Some text was available without JavaScript, but the small article section captured in the browser was entirely invisible at the moment of inspection. |
| [Flavio Bolsonaro](https://las-wb.github.io/party-ai-readiness-test/scans/04/structural.html) | Campaign text was available without JavaScript, and a sample of the linked government-plan PDF contained extractable text. Much of the inspected browser text was visually hidden. |
| [ACM Neto](https://las-wb.github.io/party-ai-readiness-test/scans/05/structural.html) | Campaign text was present in the page code, but most text in the inspected browser region was visually hidden at the moment of capture. |
| [Renan Filho](https://las-wb.github.io/party-ai-readiness-test/scans/06/structural.html) | Some text was available without JavaScript, while parts of the browser’s captured text were transparent or positioned off screen. |
| [Acir Gurgacz](https://las-wb.github.io/party-ai-readiness-test/scans/07/structural.html) | The address responded, but the browser extraction yielded no content words in the inspected region. This run provides very little evidence about readable campaign information. |
| [Orleans Brandao](https://las-wb.github.io/party-ai-readiness-test/scans/08/structural.html) | The browser captured text even though the plain response had no extracted body text, but the test could not reliably compare the two captures. |
| [Paula Belmonte](https://las-wb.github.io/party-ai-readiness-test/scans/09/structural.html) | The test was refused access to the page, so it could not assess the campaign information behind it. |
| [NOVO candidate listing](https://las-wb.github.io/party-ai-readiness-test/scans/10/structural.html) | Some party-page text was available without JavaScript, but the selected article section does not establish that the full candidate listing was captured. |
| [PCO candidate listing](https://las-wb.github.io/party-ai-readiness-test/scans/11/structural.html) | The inspected main text was available without JavaScript and was retained after browser rendering. This is the clearest text-access result in this sample. |
| [Eduardo Riedel communities page](https://las-wb.github.io/party-ai-readiness-test/scans/12/structural.html) | The requested communities address returned a not-found error, so this run could not assess its content. |
