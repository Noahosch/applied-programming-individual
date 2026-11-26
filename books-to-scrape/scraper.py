"""
Books to Scrape - scraper

Visits https://books.toscrape.com (a sandbox website made for practising
web scraping), collects every book and saves it in a local SQLite database
(books.db, created next to this file).

Run it with:  python3 scraper.py
"""

import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
DB_PATH = Path(__file__).parent / "books.db"
DELAY_SECONDS = 0.2  # small pause between requests, to be polite to the site

# The site shows ratings as a CSS class name ("star-rating Three"),
# so we translate the word into a number.
RATING_WORDS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


def get_page(session, url):
    """Download one page and return it as a BeautifulSoup object."""
    response = session.get(url, timeout=20)
    response.raise_for_status()
    # Parse the raw bytes so BeautifulSoup reads the page's own UTF-8 setting.
    # (Using response.text can turn "£" into "Â£".)
    return BeautifulSoup(response.content, "html.parser")


def get_categories(session):
    """Return a list of (category name, category URL) from the sidebar."""
    soup = get_page(session, BASE_URL)
    links = soup.select(".side_categories ul li ul li a")
    return [(a.get_text(strip=True), urljoin(BASE_URL, a["href"])) for a in links]


def parse_book(article, page_url, category):
    """Turn one <article class="product_pod"> into a dictionary."""
    link = article.select_one("h3 a")
    rating_word = article.select_one("p.star-rating")["class"][1]
    price_text = article.select_one("p.price_color").get_text(strip=True)
    stock_text = article.select_one("p.availability").get_text(strip=True)
    image = article.select_one("img")

    return {
        "title": link["title"],  # the visible text is cut off, the title attribute is complete
        "category": category,
        "price_gbp": float(price_text.replace("£", "")),
        "rating": RATING_WORDS.get(rating_word, 0),
        "in_stock": 1 if "In stock" in stock_text else 0,
        "url": urljoin(page_url, link["href"]),
        "image_url": urljoin(page_url, image["src"]),
    }


def scrape_category(session, name, url):
    """Follow a category's 'next' buttons and return all its books."""
    books = []
    while url:
        soup = get_page(session, url)
        for article in soup.select("article.product_pod"):
            books.append(parse_book(article, url, name))
        next_link = soup.select_one("li.next a")
        url = urljoin(url, next_link["href"]) if next_link else None
        time.sleep(DELAY_SECONDS)
    return books


def save_books(books):
    """Create the table if needed and insert/update every book."""
    scraped_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                price_gbp REAL NOT NULL,
                rating INTEGER NOT NULL,
                in_stock INTEGER NOT NULL,
                url TEXT NOT NULL UNIQUE,
                image_url TEXT,
                scraped_at TEXT NOT NULL
            )
            """
        )
        # The book's URL is unique, so running the scraper again updates
        # existing rows instead of creating duplicates.
        conn.executemany(
            """
            INSERT INTO books (title, category, price_gbp, rating, in_stock, url, image_url, scraped_at)
            VALUES (:title, :category, :price_gbp, :rating, :in_stock, :url, :image_url, :scraped_at)
            ON CONFLICT(url) DO UPDATE SET
                title = excluded.title,
                category = excluded.category,
                price_gbp = excluded.price_gbp,
                rating = excluded.rating,
                in_stock = excluded.in_stock,
                image_url = excluded.image_url,
                scraped_at = excluded.scraped_at
            """,
            [dict(book, scraped_at=scraped_at) for book in books],
        )
        return conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]


def main():
    session = requests.Session()
    session.headers["User-Agent"] = "books-to-scrape-student-project"

    categories = get_categories(session)
    print(f"Found {len(categories)} categories")

    all_books = []
    for i, (name, url) in enumerate(categories, start=1):
        books = scrape_category(session, name, url)
        all_books.extend(books)
        print(f"[{i}/{len(categories)}] {name}: {len(books)} books")

    total = save_books(all_books)
    print(f"Done. {len(all_books)} books scraped, {total} books in {DB_PATH.name}")


if __name__ == "__main__":
    main()
