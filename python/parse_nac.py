from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from utils.number_parser import parse_price
from utils.dates_parser import parse_datetime, NAC_FORMAT
from get_venue_id import venues
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

BASE_URL = "https://norwichartscentre.co.uk/whats-on/"

for v in venues:
    if v["venue_url"] == BASE_URL:
        venue_id = v["venue_id"]

page = 1

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page_browser = browser.new_page()

    while True:
        url = f"https://norwichartscentre.co.uk/whats-on/page/{page}/"
        print("Fetching:", url)

        page_browser.goto(url, wait_until="networkidle")
        html = page_browser.content()

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.find_all("div", class_="event-item")

        if not cards:
            print("No more pages")
            break

        for card in cards:
            title_el = card.find("a", class_="event-heading_link")
            price_el = card.find("div", class_="event-price")
            category_el = card.find_all("a", class_="nav-categories_link")
            date_time_el = card.find("div", class_="event-date")

            title = title_el.get_text(strip=True) if title_el else None
            url_link = title_el.get("href") if title_el else None
            price_text = price_el.get_text(strip=True) if price_el else ""
            min_price, max_price = parse_price(price_text)
            categories = [c.get_text(strip=True) for c in category_el]
            date_time_text = date_time_el.get_text(strip=True) if date_time_el else None
            dt = parse_datetime(date_time_text, NAC_FORMAT)

            print(title)

            cur.execute("""
                INSERT INTO events (
                    venue_id,
                    title,
                    event_datetime,
                    genre,
                    price_text,
                    min_price,
                    max_price,
                    booking_url,
                    scraped_from
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (venue_id, title, event_datetime) DO NOTHING;
            """, (
                venue_id,
                title,
                dt,
                categories,
                price_text,
                min_price,
                max_price,
                url_link,
                "norwichartscentre"
            ))

        conn.commit()
        page += 1

    browser.close()

cur.close()
conn.close()
