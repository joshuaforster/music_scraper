import os
import requests

EVENTS_URL = os.environ["EVENTS_URL"]

r = requests.get(EVENTS_URL, timeout=60)
print("status:", r.status_code)
print("body:", r.text)
r.raise_for_status()

