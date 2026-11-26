# Audit: TVmaze API (Showguide)

Before publishing, I ran the audit prompt from the submission guidelines on this folder (with Claude), fixed what it found, and ran it again.

**What was checked:** secrets and personal data, files that shouldn't be published, the `.gitignore`, dependencies and setup instructions, and the README.

## What the audit found and how I fixed it
1. **Problem:** My personal email address was in the Git commits.  
   **Fix:** I switched to my private GitHub "noreply" address and redid the commit.
2. **Problem:** My first screenshot showed my browser tabs and bookmarks.  
   **Fix:** I cropped it to show only the page.
3. **Problem:** The file was called `tv-show-explorer.html`, which isn't obvious as the file to open.  
   **Fix:** I renamed it to `index.html`.

## Second run
Everything was OK: no secrets or personal data. The TVmaze API needs no key, so there is nothing to hide.

## What I took from it
I almost published a screenshot showing all my open tabs and bookmarks, which I wouldn't have noticed without checking. It reminded me that an audit isn't only about code: everything in the repository is public, images included.

## Remaining limitations
It needs an internet connection and depends on TVmaze's free API. Finding no issues doesn't prove the project is 100% safe; it only covers what the audit checks.
