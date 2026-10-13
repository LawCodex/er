# Eritrea (ER) — legislation as Markdown

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as plain Markdown in git.

**Status: minimal.** Eritrea's legislation (proclamations and legal notices published in the *Gazette of Eritrean
Laws*, and the transitional codes of 1991 and the codes of 2015) is not published online by any official source
that could be found. This repository holds what could reliably be obtained:

* the **Constitution of Eritrea**, ratified by the Constituent Assembly on 23 May 1997 (English text). The
  Constitution has not been implemented; no official online edition exists, so the text is taken from
  **WIPO Lex** (World Intellectual Property Organization), a reputable non-official mirror;
* two legal texts published in full by the **Ministry of Information** (shabait.com): Proclamation No. 180/2017
  (stamp duty) and Legal Notice No. 124/2015 (legal tender Nakfa currency notes regulations).

Retrieved 2026-10-13.

<!-- COUNTS -->
| Directory | Files |
|---|---|
| `constitution/` | 1 |
| `legal-notices/` | 1 |
| `proclamations/` | 1 |
| **Total** | **3** |
<!-- /COUNTS -->

## Structure

```
constitution/constitution-1997.md
proclamations/<year>/<slug>.md
legal-notices/<year>/<slug>.md
```

## Sources

| Source | URL | Used for |
|---|---|---|
| WIPO Lex — Constitution of Eritrea | https://www.wipo.int/wipolex/en/text/215187 | Constitution (non-official mirror) |
| Ministry of Information of Eritrea (Shabait) | https://shabait.com/2017/03/15/proclamation-no-180-2017/ , https://shabait.com/2015/11/05/legal-notice-no-124-2015-legal-tender-nakfa-currency-notes-regulations/ | 2 legal texts |

## Not covered / known gaps

* The Gazette of Eritrean Laws, the Transitional Civil/Penal/Commercial codes and the 2015 Civil, Penal, Civil
  Procedure and Criminal Procedure Codes are not available from any official website. Unofficial copies circulate
  on third-party sites; they were not used.
* Only English texts; Tigrinya and Arabic versions (working languages) are not included.
* `status` is `unknown`: the 1997 Constitution was ratified but never entered into force.

## Copyright

Constitutional and legislative texts of the State of Eritrea are official texts. WIPO Lex provides the text for
information; it is not an official publication. The Markdown conversion is provided as is, for information.

## Regenerate

```
python3 scripts/er_fetch.py        # cache in ../_raw/er
python3 scripts/er_readme.py
```
