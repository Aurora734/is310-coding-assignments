import time
import csv

import requests
from bs4 import BeautifulSoup

from rich.console import Console
from rich.table import Table

BASE_URL = "https://wiki.leagueoflegends.com" # The main address of the wiki, which we prepend to local links.
ZAUN_LORE_URL = f"{BASE_URL}/en-us/Category:Lore_of_Zaun"
PILTOVER_LORE_URL = f"{BASE_URL}/en-us/Category:Lore_of_Piltover"
HEADERS = {
	"User-Agent": "is310-course-scraper/1.0 (student project; auroraj3@illinois.edu)"
}
REQUEST_DELAY = 1.0 # Pause between requests to avoid overwhelming the wiki's servers.
RESULTS_OUTPUT = "arcane_lore.csv" # The CSV file where we save the final list of character records.

console = Console()

'''
PLAN
 - download and parse CHECK
    - get with timesleep
    - check request status
    - parse
 - scrape subpages CHECK
    - find each page/link CHECK
 - analyze subpages CHECK
    - find each page's artifact format
    - find each page's origin (z, p, or both)
 - make counts based on origin CHECK
 - make list of all formats CHECK
 - making the table
    - 
 - make file!!
    - 
'''

# download and parse -- TBD bc it got really mad at me

def fetch_soup(url):
    if not url:
        console.print("[yellow]No URL was found for this page.[/yellow]")
        return None
	
    response = requests.get(url, headers=HEADERS, timeout=30)
    time.sleep(REQUEST_DELAY)

    if response.status_code != 200:
        console.print(f"[red]Could not download {url}: HTTP {response.status_code}[/red]")
        return None

    return BeautifulSoup(response.text, "html.parser")


# Scrape subpages
## just getting a list of dictionaries of the pages' info

def scrape_artifacts(region_page, source_url):
    artifacts = []
    if region_page is None:
        return artifacts
    
    artifacts_section = region_page.find(id="mw-pages")
    if artifacts_section is None:
        return artifacts

    artifact_items = artifacts_section.find_all("li")
    for item in artifact_items:
        link = item.find("a", href=True)
        if link is None:
            continue

        artifacts.append({
            "artifact": link.get_text(" ", strip=True),
            "artifact_url": f"{BASE_URL}{link['href']}"
        })
    
    return artifacts

# artifact origins

zaun_total = []
piltover_total = []
zaun_alone = []
piltover_alone = []
both = []

def origin(artifacts):
    # takes list of dictionaries
    for artifact in artifacts:
        soup = fetch_soup(artifact["artifact_url"])
        if soup is None:
            return artifacts # unsure about this line

        artifact_format = soup.find(id="duration").get_text()        
        if artifact_format is None:
            return artifacts # IDK!!!!!!!
        else:
            artifact["format"] = artifact_format

        cat_links = soup.find(id="mw-normal-catlinks")
        
        origin_zaun = cat_links.find(title="Category:Lore of Zaun")
        origin_piltover = cat_links.find(title="Category:Lore of Piltover")
        
        if origin_zaun is not None:
            if artifact not in zaun_total:
                zaun_total.append(artifact.get("format"))
            if origin_piltover is None:
                if artifact not in zaun_alone:
                    zaun_alone.append(artifact.get("format"))
            else:
                if artifact not in piltover_total:
                    piltover_total.append(artifact.get("format"))
                if artifact not in both:
                    both.append(artifact.get("format")) 
        elif origin_piltover is not None:
            if artifact not in piltover_total:
                piltover_total.append(artifact.get("format"))
            if artifact not in piltover_alone:
                piltover_alone.append(artifact.get("format"))
        else:
                return artifacts ## really unsure about this line

    return

# make counts

def count_formats(formats):
    quantities = {}
    short_story_count = 0

    for entry in formats:
        if "Short Story" in entry:
            short_story_count = short_story_count + 1
        elif entry not in quantities:
            amount = formats.count(entry)
            if formats.count(entry) is None:
                amount = 0
            quantities[entry] = amount

    quantities["Short Story"] = short_story_count

    return quantities

def count_totals(formats):
    total = 0
    entry_check = []

    for entry in formats:
        if entry not in entry_check:
            entry_check.append(entry)
            total = total + formats.count(entry)

    return total


# get content??

zaun_page = fetch_soup(ZAUN_LORE_URL)
zaun_artifacts = scrape_artifacts(zaun_page, ZAUN_LORE_URL)
origin(zaun_artifacts)

piltover_page = fetch_soup(PILTOVER_LORE_URL)
piltover_artifacts = scrape_artifacts(piltover_page, PILTOVER_LORE_URL)
origin(piltover_artifacts)

total_z_count = count_formats(zaun_total)
total_p_count = count_formats(piltover_total)
solely_z_count = count_formats(zaun_alone)
solely_p_count = count_formats(piltover_alone)
overlap_count = count_formats(both)

# make list of all possible formats

zaun_formats = total_z_count.keys()
piltover_formats = total_p_count.keys()
all_formats = zaun_formats

for element in piltover_formats:
    if element not in zaun_formats:
        all_formats.append(element)

# make table

table = Table(title="The Format of Lore for Zaun & Piltover")
table.add_column("Format")
table.add_column("Solely Zaun", style="magenta")
table.add_column("Zaun Total", style="green3")
table.add_column("Overlap", style="blue")
table.add_column("Piltover Total", style="gold1")
table.add_column("Solely Piltover", style="red")
table.add_column("Total")

data = []

for form in all_formats:
    if form == "":
        format_name = "Unlabeled"
    else:
        format_name = form
    
    if solely_z_count.get(form) is None:
        just_zaun = 0
    else:
        just_zaun = solely_z_count.get(form)
    
    if overlap_count.get(form) is None:
        both_regions = 0
    else:
        both_regions = overlap_count.get(form)

    if solely_p_count.get(form) is None:
        just_piltover = 0
    else:
        just_piltover = solely_p_count.get(form)

    total = just_zaun + both_regions + just_piltover

    format_row = {
        "format": format_name,
        "solely zaun": str(solely_z_count.get(form)),
        "zaun total": str(total_z_count.get(form)),
        "overlap": str(overlap_count.get(form)),
        "piltover total": str(total_p_count.get(form)),
        "solely piltover": str(solely_p_count.get(form)),
        "total": str(total)
    }

    data.append(format_row)

    table.add_row(
        format_row["format"],
        format_row["solely zaun"],
        format_row["zaun total"],
        format_row["overlap"],
        format_row["piltover total"],
        format_row["solely piltover"],
        format_row["total"],
    )

totals_row = {
    "format": "Total",
    "solely zaun": str(count_totals(zaun_alone)),
    "zaun total": str(count_totals(zaun_total)),
    "overlap": str(count_totals(both)),
    "piltover total": str(count_totals(piltover_total)),
    "solely piltover": str(count_totals(piltover_alone)),
    "total": str(
        count_totals(zaun_alone)
        +
        count_totals(both)
        +
        count_totals(piltover_alone) 
    )
}

data.append(totals_row)

table.add_row(
    totals_row["format"],
    totals_row["solely zaun"],
    totals_row["zaun total"],
    totals_row["overlap"],
    totals_row["piltover total"],
    totals_row["solely piltover"],
    totals_row["total"],
)

console.print(table)

with open(RESULTS_OUTPUT, "w", newline="", encoding="utf-8") as file:
		writer = csv.DictWriter(file, fieldnames=data[0].keys())
		writer.writeheader()
		writer.writerows(data)
