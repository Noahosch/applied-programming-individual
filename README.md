# Applied Programming and AI Fundamentals: Individual Assignment

Noah Oschinsky. Three small projects, one per folder. Each folder has its own `README.md` (what it does and how to run it) and `AUDIT.md` (the pre-publication security and quality audit).

| # | Project | What it is | Data |
|---|---|---|---|
| 1 | [Momentum Dash replica](momentum-dash/) | "Stillpoint", a Chrome new-tab extension with a clock, date and quotes | Local only, no dependencies |
| 2 | [Books to Scrape](books-to-scrape/) | Python scraper + SQLite database + local website to search the books | Unstructured HTML, structured into a database |
| 3 | [TVmaze API](tvmaze-api/) | "Showguide", a web page to explore any TV show's episodes, cast and ratings | Structured JSON from a public API |

## Repository layout
```
.
├── README.md            ← this file
├── .gitignore
├── momentum-dash/       ← Chrome extension (HTML/CSS/JS)
├── books-to-scrape/     ← Python (requests, BeautifulSoup, SQLite)
└── tvmaze-api/          ← single HTML page (JavaScript fetch)
```

No project needs an API key or account. No secrets are stored in this repository.
