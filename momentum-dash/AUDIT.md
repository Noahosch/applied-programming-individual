# Audit: Momentum Dash replica (Stillpoint)

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
| 3 | Confirmed | The README had placeholders for the Learning and Assistance sections. | `README.md` | Wrote both sections, including that the code was written with Claude. |
| 4 | Possible concern | An older copy of this project exists in a separate local repository (`Documents/GitHub/Momentum`) with uncommitted changes and a remote that was never pushed. | Outside this repository | No action needed for publication: that copy is not part of this repository. This folder is the version I'm submitting. |
| 5 | Recommendation | `manifest.json` has no icons, so Chrome shows a default icon in the extensions list. | `manifest.json` | Not fixed (cosmetic); listed as a limitation. |

"Confirmed" issues needed action before publishing. "Possible concern" and "Recommendation" items were reviewed; the table says whether they needed a change.

No secrets, keys or personal data were found. The only external resource is the background photo URL on images.unsplash.com, which is public and needs no key. The extension's Content Security Policy only allows scripts from the extension itself. No dependencies or configuration are needed.

## Round 2: re-check after fixes
The same checks were run again after the fixes and after the commit:
- Secret and personal-data search: nothing found.
- Committed files checked in GitHub Desktop: only source files, READMEs, screenshots, `.gitignore` and `.gitattributes`. No `.venv/`, `books.db`, `.DS_Store` or other local files.
- Commit author email: the GitHub `noreply` address.
- README: all seven sections present, plus a screenshot.

**Result:** no remaining issues blocking publication.

## Remaining limitations
- The background photo is hotlinked from Unsplash; if the URL ever stops working, the page falls back to a plain colour.
- No icons in the manifest (cosmetic).
- Finding no issues does not prove the project is completely safe; this audit covers the points listed above.
- Could not be verified from the audit itself: how the repository looks once it's public. I checked this separately after publishing by opening the link while logged out of GitHub.
