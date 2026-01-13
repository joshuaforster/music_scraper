import requests

url = "https://norwichartscentre.co.uk/whats-on/"

response = requests.get(url)

print(response.status_code)
print(response.text[:300])
