# Audit: Books to Scrape

Audit carried out on 26 November 2026, before publishing this repository on GitHub, using the audit prompt from the submission guidelines with Claude as the coding assistant. This file is a sanitized summary: no secret values or personal details are included.

## What was checked
The audit prompt from the submission guidelines was run from this folder's root, covering:
- Secrets, credentials, and personal or sensitive data (all files searched for keys, tokens, passwords, emails and local paths)
- Files that should be excluded (local configuration, caches, dependency folders, generated files)
- `.gitignore` rules (the repository's root `.gitignore` applies to this folder)
- Dependencies, setup instructions and configuration examples
- README sections: purpose, data collection, persistence, user interaction, setup, learning, limitations
- Git status and tracked files

The audit only read files: no project code was run, nothing was committed or pushed during the audit itself.

## Round 1: findings and fixes

| # | Type | Finding | Location | What I did |
|---|---|---|---|---|
| 1 | Confirmed | Git commits were going to be published with my personal email address (in the commit author metadata). | Repository-wide (Git config) | Switched GitHub Desktop to my GitHub private `noreply` address, undid the first commit and committed again. The published history only contains the noreply address. |
| 2 | Confirmed | The project was not yet in a Git repository, so tracked files couldn't be checked. | Repository root | Created the `applied-programming-individual` repository with GitHub Desktop and checked the list of committed files (17 files). |
| 3 | Confirmed | The folder contains a virtual environment (`.venv/`, about 15 MB of installed packages) and the generated database `books.db` (400 KB). Neither should be published. | `books-to-scrape/.venv/`, `books-to-scrape/books.db` | Both are listed in the root `.gitignore`. Checked after committing: neither appears in the tracked files. |
| 4 | Confirmed | `requirements.txt` used minimum versions (`>=`), so a future install could get different library versions. | `requirements.txt` | Pinned the exact versions I installed and tested: `requests==2.32.5`, `beautifulsoup4==4.15.0`. |
| 5 | Confirmed | The README had placeholders for the Learning and Assistance sections. | `README.md` | Wrote both sections. |
| 6 | Recommendation | The website could be exposed to other people on the network if it listened on all addresses. | `app.py` | Already safe: the server only listens on `localhost`. User input only reaches SQL through `?` placeholders, and the sort option is checked against a fixed list (no SQL injection). Book titles are HTML-escaped. |

"Confirmed" issues needed action before publishing. "Possible concern" and "Recommendation" items were reviewed; the table says whether they needed a change.

No secrets, keys or personal data were found. No account or API key is used: the data comes from a public practice website, and storage is a local SQLite file. Setup instructions cover the virtual environment, installing requirements, running the scraper and starting the website.

## Round 2: re-check after fixes
The same checks were run again after the fixes and after the commit:
- Secret and personal-data search: nothing found.
- Committed files checked in GitHub Desktop: only source files, READMEs, screenshots, `.gitignore` and `.gitattributes`. No `.venv/`, `books.db`, `.DS_Store` or other local files.
- Commit author email: the GitHub `noreply` address.
- README: all seven sections present, plus a screenshot.

**Result:** no remaining issues blocking publication.

## Remaining limitations
- `books.db` is not included, so a reviewer must run `scraper.py` first (about one minute, needs internet). This is documented in the README.
- Requires Python 3.9 or newer.
- Finding no issues does not prove the project is completely safe; this audit covers the points listed above.
- Could not be verified from the audit itself: how the repository looks once it's public. I checked this separately after publishing by opening the link while logged out of GitHub.
