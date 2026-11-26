# Audit: Books to Scrape

Before publishing, I ran the audit prompt from the submission guidelines on this folder (with Claude), fixed what it found, and ran it again.

**What was checked:** secrets and personal data, files that shouldn't be published, the `.gitignore`, dependencies and setup instructions, and the README.

## What the audit found and how I fixed it
1. **Problem:** My personal email address was in the Git commits.  
   **Fix:** I switched to my private GitHub "noreply" address and redid the commit.
2. **Problem:** The folder had files that should not be published: the virtual environment (`.venv/`) and the generated database (`books.db`).  
   **Fix:** I added them to `.gitignore` and checked that they are not on GitHub. Anyone can recreate the database by running the scraper.
3. **Problem:** `requirements.txt` didn't fix the library versions, so someone else could install different ones.  
   **Fix:** I pinned the exact versions I tested (`requests==2.32.5`, `beautifulsoup4==4.15.0`).

## Second run
Everything was OK: no secrets, no API keys (I used SQLite instead of Supabase partly for this reason), only source files tracked, and the setup steps work from a fresh download.

## Remaining limitations
The reviewer has to run the scraper first (about one minute) because the database isn't included. Finding no issues doesn't prove the project is 100% safe; it only covers what the audit checks.
