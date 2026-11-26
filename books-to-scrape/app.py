"""
Books to Scrape - web interface

A small local website to browse the books saved in books.db.
It uses only Python's standard library (no extra installs needed).

Run it with:  python3 app.py
Then open:    http://localhost:8000
"""

import html
import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DB_PATH = Path(__file__).parent / "books.db"
PORT = 8000
MAX_ROWS = 100  # show at most this many books per search

SORT_OPTIONS = {
    "title": ("Title (A-Z)", "title ASC"),
    "price_asc": ("Price (low to high)", "price_gbp ASC"),
    "price_desc": ("Price (high to low)", "price_gbp DESC"),
    "rating": ("Rating (best first)", "rating DESC, title ASC"),
}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Books to Scrape - Browser</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 0; background: #f6f5f1; color: #222; }}
  header {{ background: #24324a; color: #fff; padding: 20px 32px; }}
  header h1 {{ margin: 0; font-size: 24px; }}
  header p {{ margin: 4px 0 0; color: #c9d2e3; }}
  main {{ max-width: 1100px; margin: 0 auto; padding: 24px 32px; }}
  .stats {{ display: flex; gap: 16px; margin-bottom: 20px; }}
  .stat {{ background: #fff; border-radius: 10px; padding: 14px 18px; flex: 1; }}
  .stat b {{ display: block; font-size: 24px; }}
  form {{ background: #fff; border-radius: 10px; padding: 16px; display: flex; flex-wrap: wrap; gap: 12px; align-items: end; }}
  label {{ display: flex; flex-direction: column; font-size: 13px; color: #555; gap: 4px; }}
  input, select, button {{ font: inherit; padding: 6px 10px; border: 1px solid #ccc; border-radius: 6px; }}
  button {{ background: #24324a; color: #fff; border: 0; cursor: pointer; }}
  table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 10px; overflow: hidden; margin-top: 16px; }}
  th, td {{ text-align: left; padding: 8px 12px; border-bottom: 1px solid #eee; }}
  th {{ background: #eceae3; font-size: 13px; }}
  td img {{ height: 56px; border-radius: 3px; }}
  .stars {{ color: #d99a00; white-space: nowrap; }}
  .note {{ color: #666; font-size: 14px; }}
</style>
</head>
<body>
<header>
  <h1>Books to Scrape - Browser</h1>
  <p>Data scraped from books.toscrape.com and stored in a local SQLite database.</p>
</header>
<main>
{body}
</main>
</body>
</html>"""


def query_db(sql, params=()):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        return conn.execute(sql, params).fetchall()


def build_page(query_string):
    if not DB_PATH.exists():
        return PAGE.format(body="<p>No database found yet. Run <code>python3 scraper.py</code> first, then reload this page.</p>")

    # Read the search filters from the URL, e.g. /?q=love&category=Poetry
    params = parse_qs(query_string)
    q = params.get("q", [""])[0].strip()
    category = params.get("category", [""])[0]
    min_rating = params.get("min_rating", ["0"])[0]
    in_stock = params.get("in_stock", [""])[0] == "1"
    sort = params.get("sort", ["title"])[0]
    if sort not in SORT_OPTIONS:
        sort = "title"
    min_rating = int(min_rating) if min_rating.isdigit() else 0

    # Build the WHERE clause with "?" placeholders, so user input is never
    # pasted directly into the SQL (this prevents SQL injection).
    conditions, values = [], []
    if q:
        conditions.append("title LIKE ?")
        values.append(f"%{q}%")
    if category:
        conditions.append("category = ?")
        values.append(category)
    if min_rating:
        conditions.append("rating >= ?")
        values.append(min_rating)
    if in_stock:
        conditions.append("in_stock = 1")
    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""

    total_matches = query_db(f"SELECT COUNT(*) FROM books {where}", values)[0][0]
    rows = query_db(
        f"SELECT * FROM books {where} ORDER BY {SORT_OPTIONS[sort][1]} LIMIT {MAX_ROWS}", values
    )

    stats = query_db(
        "SELECT COUNT(*) AS n, ROUND(AVG(price_gbp), 2) AS avg_price, "
        "COUNT(DISTINCT category) AS cats, MAX(scraped_at) AS last FROM books"
    )[0]
    categories = [r["category"] for r in query_db("SELECT DISTINCT category FROM books ORDER BY category")]

    e = html.escape  # escape text so book titles can't break the page
    body = f"""
<div class="stats">
  <div class="stat"><b>{stats['n']}</b>books in the database</div>
  <div class="stat"><b>{stats['cats']}</b>categories</div>
  <div class="stat"><b>£{stats['avg_price']}</b>average price</div>
  <div class="stat"><b>{e(str(stats['last'])[:10])}</b>last scraped</div>
</div>
<form method="get">
  <label>Title contains<input name="q" value="{e(q)}" placeholder="e.g. love"></label>
  <label>Category<select name="category"><option value="">All categories</option>
    {''.join(f'<option{" selected" if c == category else ""}>{e(c)}</option>' for c in categories)}
  </select></label>
  <label>Minimum rating<select name="min_rating">
    {''.join(f'<option value="{n}"{" selected" if n == min_rating else ""}>{"Any" if n == 0 else "★" * n + " or more"}</option>' for n in range(0, 6))}
  </select></label>
  <label>Sort by<select name="sort">
    {''.join(f'<option value="{k}"{" selected" if k == sort else ""}>{label}</option>' for k, (label, _) in SORT_OPTIONS.items())}
  </select></label>
  <label><span><input type="checkbox" name="in_stock" value="1"{" checked" if in_stock else ""}> In stock only</span></label>
  <button type="submit">Search</button>
  <a href="/" class="note">Reset</a>
</form>
<p class="note">{total_matches} matching books{f", showing the first {MAX_ROWS}" if total_matches > MAX_ROWS else ""}.</p>
<table>
  <tr><th></th><th>Title</th><th>Category</th><th>Price</th><th>Rating</th><th>Stock</th></tr>
  {''.join(f'''<tr>
    <td><img src="{e(r['image_url'])}" alt=""></td>
    <td><a href="{e(r['url'])}" target="_blank" rel="noopener">{e(r['title'])}</a></td>
    <td>{e(r['category'])}</td>
    <td>£{r['price_gbp']:.2f}</td>
    <td class="stars">{"★" * r['rating']}{"☆" * (5 - r['rating'])}</td>
    <td>{"In stock" if r['in_stock'] else "Out of stock"}</td>
  </tr>''' for r in rows)}
</table>"""
    return PAGE.format(body=body)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path != "/":
            self.send_error(404)
            return
        content = build_page(url.query).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    # "localhost" means only this computer can open the site.
    server = HTTPServer(("localhost", PORT), Handler)
    print(f"Open http://localhost:{PORT} in your browser (press Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
