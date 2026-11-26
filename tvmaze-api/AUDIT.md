# Audit: TVmaze API (Showguide)

Before publishing, I ran the audit prompt from the submission guidelines on this folder (with Claude), fixed what it found, and ran it again.

## What the audit found and how I fixed it
1. **Problem:** My personal email address was in the Git commits.  
   **Fix:** I switched to my private GitHub "noreply" address and redid the commit.
2. **Problem:** My first screenshot showed my browser tabs and bookmarks.  
   **Fix:** I cropped it to show only the page.
3. **Problem:** The file was called `tv-show-explorer.html`, which isn't obvious as the file to open.  
   **Fix:** I renamed it to `index.html`.

## Second run
Everything was OK: no secrets or personal data. The TVmaze API needs no key, so there is nothing to hide.

## Remaining limitations
It needs an internet connection and depends on TVmaze's free API. Finding no issues doesn't prove the project is 100% safe; it only covers what the audit checks.
