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
 - make counts based on origin
    - 
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

zaun_total = []
piltover_total = []
zaun_alone = []
piltover_alone = []
both = []

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
        ## IMPORTANT!!! Need to figure out how to avoid 
            #repeats across multiple calls of this function
        artifacts.append({
            "artifact": link.get_text(" ", strip=True),
            "artifact_url": f"{BASE_URL}{link['href']}"
        })
    
    return artifacts

# artifact origins
def origin(artifacts):
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
        
        origin_zaun = cat_links.find(title="Category: Lore of Zaun")
        origin_piltover = cat_links.find(title="Category: Lore of Piltover")
        
        if origin_zaun is not None:
            if artifact not in zaun_total:
                zaun_total.append(artifact)

            if origin_piltover is None:
                if artifact not in zaun_alone:
                    zaun_alone.append(artifact)

            else:
                if artifact not in piltover_total:
                    piltover_total.append(artifact)
                
                if artifact not in both:
                    both.append(artifact)
        
        else:
            if origin_piltover is not None:
                if artifact not in piltover_total:
                    piltover_total.append(artifact)
            
                if artifact not in piltover_alone:
                    piltover_alone.append(artifact)
            
            else:
                return artifacts ## really unsure about this line
    
    return



# make counts
#def count_formats():
    #for 

# make table


zaun_page = fetch_soup(ZAUN_LORE_URL)
zaun_artifacts = scrape_artifacts(zaun_page, ZAUN_LORE_URL)
origin(zaun_artifacts)

piltover_page = fetch_soup(PILTOVER_LORE_URL)
piltover_artifacts = scrape_artifacts(piltover_page, PILTOVER_LORE_URL)
origin(piltover_artifacts)

print(zaun_total)
