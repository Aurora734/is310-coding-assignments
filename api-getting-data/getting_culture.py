import time

import apikey
import internetarchive
import requests
from bs4 import BeautifulSoup
from rich.console import Console


console = Console()

FANDOM_API_URL = "https://ghibli.fandom.com/api.php"
OTHER_API_BASE_URL = "https://ghibliapi.vercel.app"
## Weirdly, the params need to go after the specified enquiry endpoint rather than the base url.
OTHER_API_SPECIES_URL = "https://ghibliapi.vercel.app/species"
HEADERS = {
    "User-Agent": "is310-course/1.0 (https://Aurora734.github.io; auroraj3@illinois.edu)"
}


# MediaWiki API

response1 = requests.get(FANDOM_API_URL, params={
    "action": "query",
    "list": "categorymembers",
    "cmtitle": "Category:Species",
    "cmtype": "page",
    "cmlimit": "max",
    "format": "json",
}, headers=HEADERS, timeout=15)

console.print(response1.status_code)
if response1.status_code != 200:
    raise RuntimeError(f"API request failed: {response1.status_code}")
fandom_data = response1.json()

for page in fandom_data["query"]["categorymembers"]:
    console.print(page["title"])


# Second API

response2 = requests.get(OTHER_API_SPECIES_URL, params={
        'fields': "name,url",
        'limit': "250"
        # limit has to be an int and the max is 250
    }, headers=HEADERS, timeout=15)

console.print(response2.status_code)
if response2.status_code != 200:
    raise RuntimeError(f"API request failed: {response2.status_code}")
indie_data = response2.json()

for name in indie_data:
    console.print(name["name"])


# Specific Item = Dragons

