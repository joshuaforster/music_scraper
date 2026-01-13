import requests
from dotenv import load_dotenv
load_dotenv()

import psycopg2
import os

# Connect to your postgres DB
conn = psycopg2.connect(os.environ['DATABASE_URL'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT id, name, scrape_url FROM venues;")

# Retrieve query results
records = cur.fetchall()

cur.close()
conn.close()

venues = []

for row in records:
    venue_id = row[0]
    venue_name = row[1]
    venue_url = row[2]

    venue = {
        "venue_id": venue_id,
        "venue_name": venue_name,
        "venue_url": venue_url
    }

    venues.append(venue)

