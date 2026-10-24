import requests

HEADERS = {"User-Agent": "is310-course-scraper/1.0 (student project; auroraj3@illinois.edu)"}
response = requests.get("https://wiki.leagueoflegends.com/en-us/Category:Lore", headers=HEADERS, timeout=10)

print(response.status_code)
print(response.text[:300])