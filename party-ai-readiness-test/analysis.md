# What the twelve website checks tell us

These checks found examples of accessible text, differences between ways of reading a page, and visits that could not be assessed. They did not establish whether an AI assistant can answer a voter's questions. This is an interpretation of the saved 14 September 2026 scans from Lisbon, not a new scan or a ranking of websites.

The clearest text-access result is the PCO article: the inspected main text was already in the server response and remained available after browser rendering. Other pages also supplied text without JavaScript, but the evidence is less conclusive about coverage. For Eduardo Riedel, Time Barra and NOVO, the scanner selected an article that may cover only part of the page. A smaller extraction after rendering does not establish that the website deleted information or that AI cannot read it.

Seven captures contained visually hidden words; five crossed the detector's warning threshold. The other two still matter: Time Barra's entire small captured article was transparent, while PCO's hidden sample consisted of sharing and comment-interface labels. Warning counts are therefore a poor summary of what was found. Hidden text can remain available to a reader of the page code, and this test does not determine whether scrolling, animation or another interaction makes it visible later.

Two addresses could not be assessed: Paula Belmonte returned an access refusal (403), and Riedel's communities address returned a not-found error (404). These are results for those requests, not evidence that all AI systems are blocked or that a whole website is unavailable. Acir Gurgacz responded but yielded no browser content words in the selected region. Orleans Brandao yielded browser text, but the detector declined the before/after comparison because the browser URL ended in #/.

Nine click checks stopped because the guarded test blocked a request during loading; two more could not run on the error pages. The remaining check found no eligible control. None establishes whether voters can uncover useful information by clicking. Three PDF samples across the full scans contained extractable text, but only three pages per file were sampled. The structural report's in-region PDF example is Flavio Bolsonaro's plan: three of 76 pages inspected.

The next useful step is to inspect the actual captured passages, confirm that the correct page regions and linked documents were covered, and test specific questions against those passages. The source study's candidate inventory and declared-address categories remain a baseline; this purposive twelve-address sample does not revise the cohort percentages or measure prevalence. Its scans also cannot establish the cause of differences from earlier visits. The saved audit of the source study reported an uncoded model pilot; these website probes do not complete that evaluation.

## Each address, in plain language

### Renan Santos

Some campaign text was available without JavaScript, but the browser exposed a different mix of text and left part of it visually hidden.

The saved hidden-text sample includes campaign themes and links to videos, as well as navigation and participation prompts. These observations identify material worth checking; they do not show that a machine reader missed it. Text hidden from sight can still be present in the page code.

**Follow-up:** Check whether the captured text actually contains the proposals a voter asks about, and whether the linked videos provide information missing from the page text.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/01/structural.html)

### Eduardo Riedel

We could extract some text without running the page’s JavaScript, but this test does not establish how much useful candidate information is accessible.

The scanner inspected an article section, which may be only a small part of the page. Its two ways of reading that section returned different amounts of text. We have not established whether this reflects the website changing its content or how the scanner selects and extracts text. No visually hidden text or PDF links were found within that section.

**Follow-up:** Check the full page and identify which proposals or biographical information the reader captured before testing questions about them.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/02/structural.html)

### Time Barra / Eder Mauro

Some text was available without JavaScript, but the small article section captured in the browser was entirely invisible at the moment of inspection.

The browser document contained a short statement about security, but its styling made that text fully transparent. This could affect a reader relying on what is visible on screen; a reader of the page code may still retrieve it. The result does not establish that the entire page was blank or that the text stays invisible after interaction.

**Follow-up:** Inspect the full page and check whether scrolling or waiting reveals the section, then compare the substantive information captured by readers of the code and the visible page.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/03/structural.html)

### Flavio Bolsonaro

Campaign text was available without JavaScript, and a sample of the linked government-plan PDF contained extractable text. Much of the inspected browser text was visually hidden.

The hidden-text sample includes campaign and agenda material, alongside interface text. That is a reason to check how readers encounter the information, not proof that AI cannot retrieve it. The PDF result is encouraging for text extraction, but only three of its 76 pages were inspected; it says nothing about the remaining pages or the completeness of an answer based on the plan.

**Follow-up:** Inspect the complete plan and check whether readers can locate and accurately quote the sections needed to answer specific policy questions.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/04/structural.html)

### ACM Neto

Campaign text was present in the page code, but most text in the inspected browser region was visually hidden at the moment of capture.

The saved sample includes a substantial campaign introduction as well as participation prompts. Most of the hidden text was transparent, so a reader using only visible text could receive a much smaller account than a reader using the document. This test does not establish whether animation, scrolling or another interaction later reveals that material.

**Follow-up:** Check how the text becomes visible and whether the captured material contains concrete proposals, rather than treating the amount of text as evidence that voters’ questions can be answered.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/05/structural.html)

### Renan Filho

Some text was available without JavaScript, while parts of the browser’s captured text were transparent or positioned off screen.

The hidden-text sample mixes navigation and repeated slogans with milestones from the candidate’s career. This shows that readers using page code and visible text may encounter different material. It does not establish that important policy information is missing, or that the hidden material is inaccessible to every reader.

**Follow-up:** Check whether the career information becomes visible during ordinary browsing and whether the site offers retrievable answers about proposals beyond the biography and slogans.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/06/structural.html)

### Acir Gurgacz

The address responded, but the browser extraction yielded no content words in the inspected region. This run provides very little evidence about readable campaign information.

The absence of a hidden-text warning is not reassuring here: there were no captured content words for that check to examine. This does not prove that the website contains no information; the test did not determine why the extraction was empty.

**Follow-up:** Revisit the page and diagnose whether loading, content selection or an interaction explains the empty extraction before drawing conclusions about the site.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/07/structural.html)

### Orleans Brandao

The browser captured text even though the plain response had no extracted body text, but the test could not reliably compare the two captures.

The browser finished at an address ending in #/, which the detector treated as different from the plain request. The capture contains campaign material, much of it visually hidden, including references to proposals and a government plan. This is a lead for further inspection, not a confirmed measurement of how much JavaScript adds or whether the plan itself was read.

**Follow-up:** Resolve the address-comparison issue, inspect how the sections are revealed, and follow the plan link before assessing access to specific proposals.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/08/structural.html)

### Paula Belmonte

The test was refused access to the page, so it could not assess the campaign information behind it.

The request returned HTTP 403. Every structural check was unmeasured. This establishes a failure for this test from this connection, not that all visitors or AI services are blocked, and not that the website lacks useful content.

**Follow-up:** Investigate the access refusal and compare another permitted visit before attempting content or question-answering checks.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/09/structural.html)

### NOVO candidate listing

Some party-page text was available without JavaScript, but the selected article section does not establish that the full candidate listing was captured.

The two extractions returned different amounts of text, and the selected region was much smaller than the whole-page capture. No visually hidden text or PDF links were found within that region. Those observations do not tell us which candidates or facts were omitted, or whether the difference comes from the page or the extraction method.

**Follow-up:** Inspect the full listing and verify the names and candidate-specific facts actually captured before using this page as evidence for individual candidates.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/10/structural.html)

### PCO candidate listing

The inspected main text was available without JavaScript and was retained after browser rendering. This is the clearest text-access result in this sample.

The same extracted words were present before and after rendering. The small hidden-text sample consists of sharing and comment-interface labels, rather than evidence of hidden policy content. This supports access to the inspected article text; it does not establish that the article provides enough information about each candidate to answer a voter’s questions.

**Follow-up:** Check which candidate-specific facts the article supplies and test questions that require those facts, with answers linked back to the relevant passages.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/11/structural.html)

### Eduardo Riedel communities page

The requested communities address returned a not-found error, so this run could not assess its content.

The request returned HTTP 404 and every structural check was unmeasured. This is evidence about this particular address at the time of the visit. It does not establish that the candidate’s whole website is unavailable, or that a bot or geographic block caused the error.

**Follow-up:** Check whether the communities content moved to another address, then assess that page separately.

[Report and saved evidence](https://las-wb.github.io/party-ai-readiness-test/scans/12/structural.html)
