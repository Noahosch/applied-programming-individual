# Audit: TVmaze API (Showguide)

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
| 3 | Confirmed | The original file was named `tv-show-explorer.html`, which isn't obvious as the entry point. | `index.html` | Renamed it to `index.html` and documented how to open it. |
| 4 | Confirmed | The README had placeholders for the Learning and Assistance sections. | `README.md` | Wrote both sections. |
| 5 | Recommendation | Data from the API is inserted into the page as HTML, which could be a risk if a show's name contained HTML. | `index.html` (render functions) | Already handled: every value from the API goes through an `esc()` function that escapes HTML characters, and summaries are converted to plain text first. |
| 6 | Confirmed | The screenshot I took first showed my browser tabs and bookmarks. | `screenshots/showguide.png` | Cropped the screenshot to the page only before adding it. |

"Confirmed" issues needed action before publishing. "Possible concern" and "Recommendation" items were reviewed; the table says whether they needed a change.

No secrets, keys or personal data were found. The TVmaze API is public and needs no key. External resources are api.tvmaze.com (data and images) and Google Fonts. No dependencies or configuration are needed.

## Round 2: re-check after fixes
The same checks were run again after the fixes and after the commit:
- Secret and personal-data search: nothing found.
- Committed files checked in GitHub Desktop: only source files, READMEs, screenshots, `.gitignore` and `.gitattributes`. No `.venv/`, `books.db`, `.DS_Store` or other local files.
- Commit author email: the GitHub `noreply` address.
- README: all seven sections present, plus a screenshot.

**Result:** no remaining issues blocking publication.

## Remaining limitations
- Needs an internet connection.
- Depends on TVmaze's free API and its rate limit (documented in the README).
- Finding no issues does not prove the project is completely safe; this audit covers the points listed above.
- Could not be verified from the audit itself: how the repository looks once it's public. I checked this separately after publishing by opening the link while logged out of GitHub.
