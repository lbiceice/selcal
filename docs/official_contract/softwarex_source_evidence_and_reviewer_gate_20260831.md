# SoftwareX official evidence and reviewer gate - 2026-08-31

Status: `CURRENT GUIDE/TEMPLATES/REVIEWER FORM VERIFIED / LIVE PORTAL UNVERIFIED / PRODUCT AND SCIENTIFIC GATES HOLD`

This record supports the current SelCal product contract at the
`scientific_spine_freeze` checkpoint. It recognizes the locally tested M0-M2
implementation candidate, dependency lock, same-machine isolated installation,
documentation, examples and descriptive benchmark. It does not establish final authority
closure, scientific validity, independent reuse, release, licence, author, rights or
submission readiness.

## Current official evidence

| Source | Current direct result |
| --- | --- |
| Elsevier Research Elements page | Read on 2026-08-31; identifies SoftwareX as a multidisciplinary, open-access, peer-reviewed journal for research software and its application, and links the current Guide and template. |
| SoftwareX Guide for Authors | Read in a real browser on 2026-08-31. It retains the OSP/Software Update distinction, 4,000-word limit, six-figure cap, public-GitHub distribution, repository contents and expected Word/LaTeX roles. Automated retrieval returned HTTP 403, so the browser-visible page is the controlling read. |
| OSP DOCX | Re-downloaded and byte-matched on 2026-08-31: Version 6, March 2026; 44,823 bytes; four rendered pages; SHA-256 `9fcf40ede96a2f188ee4ef77134e0596d01e1b65fd9db63f2874d29f2ecb916d`. |
| OSP TeX | Re-downloaded and byte-matched on 2026-08-31: 10,163 bytes; SHA-256 `2b18dfd14aa3893bc4e82a90caa19337bb1ce76f1fae5ea2c0eaa7e3563b8649`. |
| Reviewer form | Re-downloaded and byte-matched on 2026-08-31: PDF 1.4; three pages; 112,676 bytes; SHA-256 `2e457d6b7bbce748dd8fa8602c76db505628cdddcd1992bdd4a2914aa2eae255`. |

Official URLs:

- <https://www.elsevier.com/researcher/author/tools-and-resources/research-elements-journals>
- <https://www.sciencedirect.com/journal/softwarex/publish/guide-for-authors>
- <https://legacyfileshare.elsevier.com/promis_misc/softwarex-osp-template.docx>
- <https://legacyfileshare.elsevier.com/promis_misc/softwarex-osp-template.tex>
- <https://legacyfileshare.elsevier.com/promis_misc/softwarex-reviewer-form.pdf>
- <https://www.editorialmanager.com/softx/default.aspx>

## Evidence layers that must not be merged

| Layer | What is supported | What remains open |
| --- | --- | --- |
| Current template | GitHub, `README.md`, `Licence.txt`, metadata C1-C8, five body sections, abstract/keyword/word/figure bounds | SelCal conformity and completed metadata |
| Current Guide | Public GitHub, `README.md`, `LICENSE.txt`, repository-root `src`, OSI-recognized source-code licence and expected upload roles | Live SelCal portal configuration and omitted licence-name list |
| Internal reproducibility control | Exact release/tag freezing, byte manifests and a PID where available | These controls must not be mislabeled as journal-explicit hard rules |
| Author and rights facts | The user described SelCal as new software | Formal no-prior-SoftwareX genealogy, authorship, rights, code-licence choice and article-licence choice |

The source-code licence and the open-access article licence are separate decisions. The
Guide/template `LICENSE.txt` versus `Licence.txt` naming conflict remains open; only after
the rights holder selects the source-code licence may same-content compatibility files be
created.

## Portal boundary

The current Guide states expected Word and LaTeX file roles. Those statements do not prove
the live configuration of a future SelCal Editorial Manager draft. The current article
type, author fields, declarations, file designations, supplementary slots and generated
review PDF must be captured from a fresh draft when the portal gate becomes due.

## Reviewer-form consequences

| Gate | Required evidence before manuscript or release closure |
| --- | --- |
| Scientific impact | Prospective M6 results tied to new or improved research questions, a comparator delta and a bounded reuse claim |
| Empirical evaluation | Clear setting, exact-oracle checks, prior-work comparison, retained adverse results and claim-proportionate interpretation |
| Install and reproduce | Independent clean installation on declared platforms and replay of documented examples with compatible outputs |
| Portability | Explicit interpreter and operating-system matrix with failures preserved |
| Testing and documentation | Test programs exercising all main features, API/user documentation, environment and dependency identity |
| Licensing and provenance | Author-selected source-code licence, dependency licence inventory, exact source manifest and licence identification in the package |
| Metadata and artifacts | Complete C1-C8, public GitHub URL, support contact, data and documentation bound to the exact release |

## Current SelCal consequence

The official-source identity is current, but the contract remains `HOLD`. The next product
gate is Task-10 scope-v2 authority closure. M3 event/resume, M4 evidence bundles, the M5
CLI, prospective M6 evidence, independent/cross-platform installation, public release,
source-code licence, rights, authorship and portal evidence remain open. No manuscript
content or upload-ready package is authorized by this refresh.
