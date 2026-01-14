import subprocess
import requests
import os

print("Running scraper...")
subprocess.check_call(["python", "parse_nac.py"])

print("Triggering email send...")
EVENTS_URL = os.environ["EVENTS_URL"]

r = requests.get(EVENTS_URL, timeout=60)
print("Email endpoint status:", r.status_code)
print("Email endpoint response:", r.text)
r.raise_for_status()
