# Party Web Readiness Check

We checked **12 web addresses** using two assessments: the **full LAS test** and the smaller **“Can AI read it?” structural test**. This folder contains the 24 reports, their results and supporting evidence, plus an assessment of the source repository.

To browse the reports after downloading or checking out this PR, serve this folder locally and open the index:

```sh
python3 -m http.server 8011 --bind 127.0.0.1 --directory party-ai-readiness-test
```

Then open `http://127.0.0.1:8011/index.html`. The saved HTML reports do not require the LAS application to be running.

**My assessment: a substantial and useful study of declared web presence, with much narrower evidence about how well AI systems actually inform people.** Its strongest contribution is the candidate census and its explicit, reproducible classification rules. It is less thorough about information inside each site, and its model-answer evaluation is unfinished.

[Open the 12-site report index](index.html) · [Scan comparison](scan-comparison.md) · [Machine-readable audit](data-audit.json)

## Where it is and what it is

- GitHub: **[participatory/party-web-ai-readiness](https://github.com/participatory/party-web-ai-readiness)**, a private repository under `participatory`, on `main`.
- Reviewed snapshot: `169007110e2ccfeafa8d39ba83f4cb9e21012f4f`, pushed 13 September 2026. The original archive and unpacked copy are retained locally and excluded from this PR; the source repository is linked above.
- Package location in LAS-WB/las: `party-ai-readiness-test/`.
- Intended work: a study for **ITS Rio** of the web presence of Brazil's 2026 presidential, gubernatorial and Senate candidate cohort. It contains data, Python collection/classification scripts, methodological decisions, an API pilot, research-assistant worksheets and publication drafts. It is not a deployed scanning application. I found draft outputs, not an established public deployment address.

The GitHub description still calls it a ranking. The latest decision and generated output explicitly use **seven descriptive categories**, with no numerical candidate rank. I used those current outputs, rather than earlier proposals, for this review.

## How much data there is

I structurally audited every CSV, JSON and JSONL record in the snapshot: 23 CSV files, 22 JSON files and four JSONL files. This includes checking completeness and consistency; it does not mean I fact-checked every model answer.

| Layer | Verified contents | What it can tell us |
|---|---|---|
| Candidate frame | 527 unique IDs: 13 presidential, 197 gubernatorial and 317 Senate records; 29 parties | Which declared addresses and party coverage are attached to the study cohort |
| Website sweep | 272 distinct URLs, 263 hosts, 33 recorded fields per URL | HTTP outcomes, redirects, served text, metadata, JSON-LD, PDF-link counts, crawler policy and discovery-file presence |
| Party coverage | 28 party-site sweep rows, 696 party-crawl records, 198 saved party-page text files | Additional candidate references and evidence for qualifying party coverage |
| Question collection | 779 prompt records; 24 prompts in the reviewed pilot selection, 22 used in single-candidate calls | A documented question corpus, with review and decomposition of compound questions |
| Current API pilot | 1,584 unique responses: 12 candidates × 22 prompts × 3 models × 2 repetitions | What those model/configuration combinations answered to those prompts |
| Follow-up fieldwork | 165 site-search assignments, 12 candidates for 96 planned consumer-assistant observations | A plan to investigate omissions and real consumer behavior; those results are not yet present |

The four rows in the supplemental site sweep also appear in the 272-row table. They are **not four additional distinct sites**. Archived API arms and error logs are likewise separate from the current 1,584 responses.

## What the current website results say

| Final category | Candidates |
|---|---:|
| Own readable site, with sitemap or JSON-LD | 83 |
| Own readable site, without those signals | 32 |
| Qualifying party page only | 21 |
| Live address, without qualifying own text | 52 |
| Address returned an error at the visit | 16 |
| Bot check stopped the reader | 10 |
| No website-like address declared, after the category rules | 313 |
| **Total** | **527** |

I independently reproduced the category assignments from their stored input flags: no differences. The candidate tables also join on the same 527 unique IDs without missing or duplicate records.

The headline is **391/527, or 74.2%, without qualifying content retrieved under this protocol**. This is not a website failure rate. The final negative categories include 313 candidates without a declared website-like address. At the source-frame level, 335 have no declared website and 192 have one; party coverage and category precedence explain why those counts differ from the final table. A missing declared address is not proof that a website does not exist, and social-media addresses are a different field.

“Substantive” means at least 100 extracted words, subject to authorship and coverage exclusions. Using 20 or 300 words changes the headline to 72.1% or 77.6%. That sensitivity is useful: the broad pattern survives, while the precise classification depends on a declared threshold. A hundred words does not establish that a page answers a voter's question.

## What is thorough, and what is missing

**The collection design is comparatively careful.** It records URLs, times, user agents, HTTP outcomes and errors, retries address variants, separates challenges from declared crawler policy, filters shared candidate/party material, and keeps review decisions and superseded model runs. The latest revision fixed stale party evidence and stopped awarding structure credit from a different, unreadable domain. Those are meaningful safeguards.

**The website inspection is shallow by design.** Its primary reader fetches server-sent HTML without rendering JavaScript, clicking controls or following content links. The extractor skips scripts and related elements but is not a semantic assessment of the candidate's substantive information. PDF links are counted; their contents are not examined by that sweep. Sitemap/JSON-LD presence does not verify completeness, correctness, candidate-specific facts, or any improvement in an assistant's answer. Discovery-file detection is largely an HTTP/content-type presence check.

**The raw evidence needed for complete replay is missing from GitHub.** The main sweep references 239 saved page files and 176 robots files; none is included. The party and supplemental sweep references are also absent. `.gitignore` excludes the page archive and raw source data. The saved party text, derived tables and code are useful, but this snapshot cannot independently establish everything claimed about the original HTML, robots templates or source extraction. The original author may have those files locally.

**The model pilot is complete as a collection, unfinished as an evaluation.** GPT-5, Gemini 2.5 Flash and DeepSeek Chat v3.1 each have 528 current responses. All expected cells exist, all are nonempty, none records an API error, and every finish reason is `stop`. All current arms use a 4,000-token maximum, although reasoning settings differ. Crucially, **all 1,584 responses are marked `uncoded`**. There is no completed, adjudicated accuracy or unsupported-claim rate here. These API calls test model knowledge without the consumer browsing workflow; they do not test whether a model could read the candidate's website. The prompt corpus is also not a representative sample of Brazilian voter demand.

**The checks that could close the largest gaps are still pending.** All result fields in the 165-row site-search worksheet are blank. The consumer-assistant CSV lists candidates, not observations. The original 86-row party worksheet is blank; a separate file contains five party-level inspection summaries. Those summaries support “no qualifying page found during this inspection,” not exhaustive absence. The repo acknowledges an unresolved consistency problem between counting candidacy news in automated coverage and dismissing news-only material in some manual checks.

**A few consistency issues remain.** One JSON file, `party-candidate-pages.json`, fails strict UTF-8 decoding; the audit records the exact error and a two-character lossy recovery without changing the original. `fieldwork.json` retains the earlier population of 390 while current outputs use 391. The decision note says six party-site and four own-site bot checks, while the generated summary says five and five. The draft HTML also retains broad free-versus-paid assistant claims alongside a later, more appropriate caveat. These should be reconciled before publication; they are not evidence that the 527-row arithmetic is wrong.

## What LAS adds, and how to read these new reports

The dozen addresses were chosen for variation: readable candidate sites, sparse/empty responses, a challenge, an error page, PDF links and shared party articles. They are traceable to source records in [selected-urls.json](selected-urls.json). This is a purposive test set, not a prevalence estimate. Candidates with no address cannot be directly URL-tested.

Each address went through the existing LAS scanner with D/L/O/N/T enabled, without AI model calls, from **residential, Lisbon**, on 14 September 2026. The same address fills LAS's homepage and service-page inputs. Each run saves the raw structured capture, profile, full LAS report and structural report. No earlier scan profile was reused. The scanner commit is `6fa2f72`; detector versions and run IDs are inside each output. The full LAS HTML adds a prominent tested URL and a scope note for this batch; the underlying measurements and standard report body are preserved.

**All 12 runs completed and produced 24 reports.** Ten requested pages returned HTTP 200, Paula Belmonte returned 403, and the Eduardo Riedel communities page returned 404. Five sites raised the hidden-text advisory. Eleven click checks are unmeasured: nine because the guarded probe blocked requests during page loading, and two because the page could not be read. The remaining click check found no applicable control. These are distinct outcomes, not twelve successful content assessments.

LAS adds served/rendered comparisons, hidden-text observations, guarded click probes, bounded route crawling and sampled PDF extraction. It provides a more useful account of *how* content is exposed. It still does not establish whether that content is complete, true, easy to discover in search, cited by an assistant, or sufficient to answer a voter.

The fresh tests also reveal limits in our own instrument:

- Several campaign pages use an `article` that covers only a small part of the document. Our scoped numbers and the original whole-page counts should not be treated as interchangeable.
- Click measurements often stop when load-time POST requests are blocked. This is a measurement gap, not a finding that information is buried behind a click.
- Orleans Brandao's raw response has zero extracted body words, while the browser captures content at a `#/` URL. Our detector declines that comparison because the final URLs differ. The captures are informative; the detector's conclusion remains unmeasured.
- The three sampled PDFs contain extractable text. Sampling three pages per file is not a complete document audit. A PDF outside the chosen main region may appear in the full LAS evidence but be out of scope for the structural PDF check.
- Application forms, login and application-route depth come from LAS's government-service design. They should not be used to judge campaign-site quality. For example, LAS labels PCO's `/contato/` contact form as an application entry; that is not evidence of a relevant service application. The full report retains that standard wording and scoring.
- LAS's named-crawler probes use user-agent strings from our local connection. They do not originate from verified vendor crawler infrastructure and do not test actual consumer assistants.
- The legacy LAS report speculates about a disguised block when describing the communities page's 404. The observation establishes an HTTP error, not its cause. That report has an explicit scope note clarifying this limitation.

The standard reports retain all measurement gaps. **No detector warning is not an all-clear.** Changes since the earlier crawl can reflect site edits, network differences, redirects, timing or different extraction scopes. This comparison cannot retrospectively invalidate the earlier measurements.

For this project's goal, I would use the repository as the **candidate inventory and documented baseline**, LAS as the **structural inspection layer**, and completed, adjudicated question-and-answer tests as the **outcome layer**. Before publishing stronger AI-readiness claims, the priorities are to preserve the missing source evidence, finish answer coding and consumer observations, verify candidate-specific information, and reconcile the remaining draft inconsistencies.

## Files and reproduction

The published structural reports lead with all recorded measurements, including observations below detector warning thresholds, followed by the limits of the tests. Run `python party-ai-readiness-test/present_results.py` to rebuild this presentation from the saved evidence without scanner dependencies or network access. `build_results.py` also runs this step. Raw scans, profiles, detector states and scan dates are unchanged. The original verification captures document the first publication; `verification/presentation-verification.json` and `measurement-summary-*.png` record the updated presentation checks.

- [index.html](index.html): browse all structural and LAS reports.
- [scan-comparison.md](scan-comparison.md), [comparison.csv](comparison.csv), [comparison.json](comparison.json): old and fresh measurements, with scope and gaps.
- `scans/01/` through `scans/12/`: `structural.html`, `LAS.html`, `raw.json`, `profile.json`, `structural-view.json`, `result.json`.
- [data-audit.json](data-audit.json), [test-summary.json](test-summary.json), [scan-results.json](scan-results.json): audit and execution records.
- `repository/` and `repository.tar.gz`: local-only private source snapshot, excluded from version control; no source files were modified. To rerun the source audit or URL selection, obtain the pinned source commit with authorized access and unpack it into `repository/` first.
- `audit_repository.py` and `build_results.py`: regenerate the local audit and index from saved data. `run_las.py` runs the fixed sample and skips completed results on resume. Scanner and renderer reproduction require the LAS implementation at `6fa2f72` (report implementation PR #32) and its dependencies; the saved reports themselves are standalone. Fresh scanning also requires network/browser access.

The shareable findings, report evidence and reproduction scripts are contained in this folder. Local source copies, logs and temporary execution files are excluded from the PR.
