import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

console = Console()
output_file = Path("tv_shows.json")

# starting dictionary with examples
shows = [
    {
        "title": "Friends",
        "release_start": 1994,
        "release_end": 2004,
        "seasons_count": 10,
        "genre": "situational comedy",
        "premise": "six friends lives in NYC through their twenties and thirties",
    },
    {
        "title": "Buffy the Vampire Slayer",
        "release_start": 1997,
        "release_end": 2003,
        "seasons_count": 7,
        "genre": "vampire horror",
        "premise": "a girl with the power to slay vampires must protect the world from demons",
    }
]

# display table of shows
def display(series_data):
    # table
    table = Table(title="Television Series")
    table.add_column("Title", style="magenta")
    table.add_column("Release Year(s)", style="green")
    table.add_column("Number of Seasons", style="yellow")
    table.add_column("Genre", style="cyan")
    table.add_column("Premise", style="blue")
    # putting starting examples in table
    for series in series_data:
        table.add_row(
            series["title"],
            str(series["release_start"]) + "-" + str(series["release_end"]),
            str(series["seasons_count"]),
            series["genre"],
            series["premise"]
        )
    
    console.print(table)

# showing examples to user
console.print("Current data:")
display(shows)

# input process
def collect_series():
    title = console.input(prompt='[bold]Title of series:[/bold] ').strip()
    release_start = console.input(prompt='[bold]Starting year of release:[/bold] ').strip()
    release_end = console.input(prompt='[bold]Ending year of release:[/bold] ').strip()
    seasons_count = console.input(prompt='[bold]Number of seasons:[/bold] ').strip()
    genre = console.input(prompt='[bold]Genre:[/bold] ').strip()
    premise = console.input(prompt='[bold]Short premise:[/bold] ').strip()

    show = {
        "title": title,
        "release_start": int(release_start),
        "release_end": int(release_end),
        "seasons_count": int(seasons_count),
        "genre": genre,
        "premise": premise
    }

    return show

def confirm_data(show):
    console.print("[bold orange]Please review the data you've entered and confirm it is correct:[/bold orange]")
    display([show])
    confirmation = console.input("Is this correct? Enter yes or no: ").strip().lower()
    return confirmation in ["yes", "y"]

for entry_number in range(2):
    console.print(f"[bold]Add television series {entry_number + 1} of 2[/bold]")
    new_show = collect_series()
    confirmed = confirm_data(new_show)

    if confirmed is False:
        console.print("[bold red]Please re-enter the series' information:[/bold red]")
        new_show = collect_series()
        confirmed = confirm_data(new_show)

    if confirmed:
        shows.append(new_show)
        console.print("[bold green]Television series added[/bold green]")
    else:
        console.print("[bold red]Television series not saved[/bold red]")

output_file.write_text(json.dumps(shows, indent=4), encoding="utf-8")
console.print(f"File saved at {output_file.resolve()}")