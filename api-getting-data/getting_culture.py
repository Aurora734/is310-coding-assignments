import time

import apikey
import internetarchive
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
import csv

console = Console()

FANDOM_API_URL = "https://ghibli.fandom.com/api.php"
OTHER_API_BASE_URL = "https://ghibliapi.vercel.app"
## Weirdly, the params need to go after the specified enquiry endpoint rather than the base url.
OTHER_API_SPECIES_URL = "https://ghibliapi.vercel.app/species"
HEADERS = {
    "User-Agent": "is310-course/1.0 (https://Aurora734.github.io; auroraj3@illinois.edu)"
}
RESULTS_OUTPUT = "dragon_comparison.csv"

# MediaWiki API

response1 = requests.get(FANDOM_API_URL, params={
    "action": "query",
    "list": "categorymembers",
    "cmtitle": "Category:Species",
    "cmtype": "page",
    "cmlimit": "max",
    "format": "json",
}, headers=HEADERS, timeout=15)

console.print("[magenta]Ghibli Fandom page status code: [/magenta]", response1.status_code)
if response1.status_code != 200:
    raise RuntimeError(f"[red]API request failed: {response1.status_code}[/red]")
fandom_data = response1.json()

console.print("[magenta]Ghibli Fandom page species:[/magenta]")
for page in fandom_data["query"]["categorymembers"]:
    console.print(page["title"])


# Second API

response2 = requests.get(OTHER_API_SPECIES_URL, params={
        'fields': "id,name,classification,eye_colors,hair_colors,url,people,films",
        'limit': "250"
        # limit has to be an int and the max is 250
    }, headers=HEADERS, timeout=15)

console.print("[magenta]Studio Ghibli API status code: [/magenta]", response2.status_code)
if response2.status_code != 200:
    raise RuntimeError(f"[red]API request failed: {response2.status_code}[/red]")
indie_data = response2.json()

console.print("[magenta]Studio Ghibli API species:[/magenta]")
for species in indie_data:
    console.print(species["name"])


# Specific Item = Dragons

dragon_films = []

# sorry to hard-code, but that's essentially what the API site is telling me to do to  find a specific species' info
INDIE_DRAGON_URL = OTHER_API_SPECIES_URL + "/e2cfaa78-fb19-11eb-9a03-0242ac130003"

response3 = requests.get(INDIE_DRAGON_URL, params={
        'fields': "id,name,classification,eye_colors,hair_colors,url,people,films",
    }, headers=HEADERS, timeout=15)

console.print("[magenta]Studio Ghibli API Dragon status code: [/magenta]", response3.status_code)
if response3.status_code != 200:
    raise RuntimeError(f"[red]API request failed: {response3.status_code}[/red]")
indie_dragon = response3.json()

indie_dragon_film_urls = indie_dragon["films"]

OTHER_API_FILMS_URL = "https://ghibliapi.vercel.app/films"
response4 = requests.get(OTHER_API_FILMS_URL, params={
        "fields": "id,title,original_title,original_title_romanized,species,url",
        "limit": "250"
    }, headers=HEADERS, timeout=15)

console.print("[magenta]Studio Ghibli API films status code: [/magenta]", response4.status_code)
if response4.status_code != 200:
    raise RuntimeError(f"[red]API request failed: {response4.status_code}[/red]")
indie_films = response4.json()

indie_dragon_films = []
for film in indie_films:
    if film["url"] in indie_dragon_film_urls:
        indie_dragon_films.append(film["title"])
        dragon_films.append(film['title'])

console.print("[magenta]Studio Ghibli API Dragon films:[/magenta]", indie_dragon_films)

response5 = requests.get(FANDOM_API_URL, params={
        "action": "parse",
        "page": "dragons",
        "prop": "text|links|langlinks",
        "format": "json",
    }, headers=HEADERS, timeout=15)

if response5.status_code != 200:
    console.print(f"[red]API request failed: {response5.status_code}[/red]")
fandom_dragons = response5.json()

if "error" in fandom_dragons:
    console.print(f"[red]Could not parse dragons: {fandom_dragons['error']['info']}[/red]")

page = fandom_dragons["parse"]
html = page["text"]["*"]
soup = BeautifulSoup(html, "html.parser")

appearances = soup.find(id="Appearances")
h2_appearances = appearances.find_parent("h2")

fandom_dragon_films = []

for next_heading in h2_appearances.find_all_next(["h2", "h3"]):
    # A new major section means Appearances has ended.
    if next_heading.name == "h2":
        break

    # Use the headline span to exclude the heading's edit link.
    headline = next_heading.find(class_="mw-headline")
    if headline is None:
        headline = next_heading

    fandom_dragon_films.append(
        headline.get_text(" ", strip=True)
    )

console.print("[magenta]Fandom dragon films:[/magenta]", fandom_dragon_films)

# let's pretend I got the Fandom dragon films to work and they are held in the following list
for film in fandom_dragon_films:
     if film not in indie_dragon_films:
          dragon_films.append(film)

dragon_films.sort()
console.print(dragon_films) # to double check

table = Table(title="Comparing Lists of Dragon Film Appearances")
table.add_column("API")
for film in dragon_films:
     table.add_column(film, style='green')

def analyze_film_list(list, api_name):
     list_booleans = {
          "API": api_name
     }

     for film in dragon_films:
         if film in list:
             list_booleans[film] = True
         else:
             list_booleans[film] = False

     return list_booleans

indie_booleans = analyze_film_list(indie_dragon_films, "Studio Ghibli API")
fandom_booleans = analyze_film_list(fandom_dragon_films, "Ghibli Fandom")

data = []
data.append(fandom_booleans)
data.append(indie_booleans)

console.print(fandom_booleans)
console.print(indie_booleans)

table.add_row(
     str(fandom_booleans['API']),
     str(fandom_booleans['Castle in the Sky']),
     str(fandom_booleans['Pom Poko']),
     str(fandom_booleans['Spirited Away']),
     str(fandom_booleans['Tales from Earthsea']),
     str(fandom_booleans['The Tale of the Princess Kaguya']),
)

table.add_row(
     str(indie_booleans['API']),
     str(indie_booleans['Castle in the Sky']),
     str(indie_booleans['Pom Poko']),
     str(indie_booleans['Spirited Away']),
     str(indie_booleans['Tales from Earthsea']),
     str(indie_booleans['The Tale of the Princess Kaguya']),
)

# make table appear
console.print(table)

with open(RESULTS_OUTPUT, "w", newline="", encoding="utf-8") as file:
		writer = csv.DictWriter(file, fieldnames=data[0].keys())
		writer.writeheader()
		writer.writerows(data)