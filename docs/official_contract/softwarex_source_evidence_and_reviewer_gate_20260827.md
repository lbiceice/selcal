# SoftwareX official evidence and reviewer gate - 2026-08-27

Status: `OFFICIAL GUIDE VERIFIED / PRODUCT AND SCIENTIFIC GATES HOLD`

This record supports the SelCal product contract at the `scientific_spine_freeze`
checkpoint. It does not establish implementation, scientific validity, repository
release, author or rights approval, or submission readiness.

## Current official evidence

| Source | Direct result |
| --- | --- |
| Elsevier Research Elements page | Read on 2026-08-27; identifies SoftwareX as a multidisciplinary, open-access, peer-reviewed journal for detailed research-software articles and links the current Guide and template. |
| SoftwareX Guide for Authors | Read in a real browser on 2026-08-27. Ordinary automated retrieval still returned HTTP 403, so the browser-visible official page is the controlling current read. |
| OSP DOCX | Version 6, March 2026; 44,823 bytes; four pages rendered and inspected; SHA-256 `9fcf40ede96a2f188ee4ef77134e0596d01e1b65fd9db63f2874d29f2ecb916d`; server Last-Modified `2026-04-17T10:28:21Z`. |
| OSP TeX | 10,163 bytes; SHA-256 `2b18dfd14aa3893bc4e82a90caa19337bb1ce76f1fae5ea2c0eaa7e3563b8649`; server Last-Modified `2026-04-17T10:29:37Z`. |
| Reviewer form | PDF 1.4; three pages rendered and inspected; 112,676 bytes; SHA-256 `2e457d6b7bbce748dd8fa8602c76db505628cdddcd1992bdd4a2914aa2eae255`. |

Official URLs:

- <https://www.elsevier.com/researcher/author/tools-and-resources/research-elements-journals>
- <https://www.sciencedirect.com/journal/softwarex/publish/guide-for-authors>
- <https://legacyfileshare.elsevier.com/promis_misc/softwarex-osp-template.docx>
- <https://legacyfileshare.elsevier.com/promis_misc/softwarex-osp-template.tex>
- <https://legacyfileshare.elsevier.com/promis_misc/softwarex-reviewer-form.pdf>
- <https://www.editorialmanager.com/softx/default.aspx>

## Product identity and structure

SelCal is a conditional candidate for `Original Software Publication`, which the Guide
specifies for new unpublished software. `Software Update` applies only to software
previously published in SoftwareX.

The submission has two inseparable products:

1. a short descriptive paper with a 4,000-word limit; and
2. an open-source software distribution with support material.

The mandatory manuscript sections are:

1. Motivation and significance;
2. Software description, including architecture and functionality;
3. at least one Illustrative example;
4. Impact; and
5. Conclusions.

The current templates also require complete metadata C1-C8, an approximately 100-word
abstract, no more than six keywords, no more than six figures, and a public GitHub
repository. The Guide counts the abstract, running text, captions and footnotes within
the 4,000 words, while excluding the title, authors, affiliations, references and
metadata tables.

## Reviewer-form rules written back into the SelCal gate

The official reviewer form is converted into the following development exit rules.
None may be satisfied by manuscript prose alone.

| Gate | Required evidence before release or manuscript work |
| --- | --- |
| Scientific impact | Prospective M6 results tied to new or improved research questions, a comparator delta and a bounded reuse claim. |
| Empirical evaluation | Clear experimental setting, exact-oracle checks, comparison with prior work, retained adverse results and results proportional to the claim. |
| Install and reproduce | Independent clean installation on the declared platforms and replay of documented examples with compatible outputs. |
| Portability | Explicit supported interpreter and operating-system matrix with failures preserved. |
| Functional testing | Automated tests that exercise every public main feature; coverage percentage alone is insufficient. |
| Documentation | README purpose, installation and use; API documentation; developer documentation or manual; environment and dependency identity. |
| Maintainability | Readable source, stable public contracts, release notes, error semantics and a bounded compatibility policy. |
| Licensing and provenance | Author-selected OSI-recognized code licence, dependency licence inventory, exact source manifest and licence identification in the source package. |
| Non-code artifacts | Validation data, examples, configuration, figures and documentation bound to the exact release. |
| Metadata | Complete and mutually consistent C1-C8 values, public GitHub URL and support contact. |

The reviewer form separately rates manuscript quality and submitted-software quality.
Therefore a strong paper cannot compensate for weak software, and a locally clean code
base cannot compensate for absent impact evidence.

## Current conflicts and conservative resolution

1. The Guide requires `LICENSE.txt`; both current templates require `Licence.txt`.
   Preserve this conflict. After the author selects the code licence, produce compatible
   same-content files and make CI verify their byte equality. Do not select a licence on
   the author's behalf.
2. The Guide says approved licences are listed below, but the live page contains no
   licence-name list and only links the Open Source Initiative. Apache, GPL and MIT in
   the Word template are examples, not an exhaustive authorization list.
3. The Word journal-specific instruction requires figures embedded in the DOCX, while
   the generic figure section asks for separate files. Keep embedded figures and
   separate source-quality figure files until the live portal slot map is captured.
4. GitHub is mandatory for metadata C2. A DOI or other persistent identifier is strongly
   preferred for software citation but does not replace C2. Freeze a release or tag as a
   reproducibility control without calling the tag requirement an explicit journal rule.

## SelCal consequence

The current architecture order remains correct:

`M0-M2 scientific core -> M3-M5 execution/evidence/API -> M6 impact and product validation -> M7 UI and M8 release/manuscript`

The official Guide is no longer the blocking unknown. The controlling blockers are now
SelCal's unimplemented full-reselection core, unexecuted M6 evidence, absent public
release and clean-install evidence, and unresolved author-owned licence and declarations.
