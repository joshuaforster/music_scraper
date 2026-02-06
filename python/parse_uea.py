from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from utils.number_parser import parse_price
from utils.dates_parser import parse_datetime
from get_venue_id import venues
from dotenv import load_dotenv
import psycopg2
import os
import time

# -------------------------
# Setup
# -------------------------

load_dotenv()

conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

BASE_URL = "https://www.ueaticketbookings.co.uk/whats-on/"
GENRE = "Reggae"

for v in venues:
    if v["venue_url"] == BASE_URL:
        venue_id = v["venue_id"]

# UEA date format example:
# "Fri 20 February 2026 7:30pm"
UEA_FORMAT = "%a %d %B %Y %I:%M%p"

page_number = 1

# -------------------------
# Scraper
# -------------------------

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )

    page_browser = browser.new_page()

    while True:
        list_url = (
            "https://www.ueaticketbookings.co.uk/whats-on"
            "?_sfm_venue=The%20Nick%20Rayns%20LCR%2C%20UEA"
            f"&_sfm_genre={GENRE}"
            f"&sf_paged={page_number}"
        )

        print("Fetching list page:", list_url)

        page_browser.goto(list_url, wait_until="networkidle")
        soup = BeautifulSoup(page_browser.content(), "html.parser")

        cards = soup.find_all("div", class_="event_item")

        if not cards:
            print("No more pages")
            break

        for card in cards:
            # -------------------------
            # Basic card data
            # -------------------------

            title_el = card.find("h4")
            link_el = card.find("div", class_="event_thumb").find("a")
            date_el = card.find("div", class_="when")
            status_el = card.find("div", class_="event_btns")

            title = title_el.get_text(strip=True) if title_el else None
            url_link = link_el.get("href") if link_el else None
            date_text = date_el.get_text(" ", strip=True) if date_el else None
            status_text = status_el.get_text(strip=True).lower() if status_el else ""

            if not title or not url_link:
                continue

            # -------------------------
            # Availability filter
            # -------------------------

            allowed_statuses = [
                "book tickets",
                "selling fast",
                "last few",
            ]

            blocked_statuses = [
                "sold out",
                "cancelled",
                "postponed",
                "new date",
            ]

            if any(bad in status_text for bad in blocked_statuses):
                continue

            if not any(ok in status_text for ok in allowed_statuses):
                continue

            # -------------------------
            # Visit event page
            # -------------------------

            print("  Visiting event:", title)

            page_browser.goto(url_link, wait_until="networkidle")
            time.sleep(0.5)

            event_soup = BeautifulSoup(page_browser.content(), "html.parser")

            # -------------------------
            # Date + time (prefer event page)
            # -------------------------

            when_el = event_soup.find("div", class_="when")

            if when_el:
                when_text = when_el.get_text(" ", strip=True)
                dt = parse_datetime(when_text, UEA_FORMAT)
            else:
                dt = parse_datetime(date_text, "%a %d %B %Y")

            # -------------------------
            # Price extraction
            # -------------------------

            ticket_row = event_soup.find("div", class_="TicketType")

            if not ticket_row:
                continue

            price_el = ticket_row.find("span", class_="Price")
            price_text = price_el.get_text(strip=True) if price_el else ""

            if not price_text:
                continue

            min_price, max_price = parse_price(price_text)

            # -------------------------
            # Insert
            # -------------------------

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
                [GENRE],
                price_text,
                min_price,
                max_price,
                url_link,
                "uea"
            ))

            conn.commit()

        page_number += 1

    browser.close()

cur.close()
conn.close()
