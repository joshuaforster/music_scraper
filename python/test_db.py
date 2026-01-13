import requests
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

# Connect to your postgres DB
conn = psycopg2.connect(os.environ['DATABASE_URL'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT id, name, scrape_url FROM venues;")

# Retrieve query results
records = cur.fetchall()

for row in records:
    venue_name = row[1]
    venue_url = row[2]

    print("\n====================")
    print(venue_name)
    print(venue_url)

    response = requests.get(venue_url)

    print("Status:", response.status_code)
    print("TEXTT", response.text[:300])

cur.close()
conn.close()