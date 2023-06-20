# Slot Checker

## What does it do?

The script checks wether the iframes of a list of slot games are set up correctly.

*Please note*: The script catches only errors if the slot games are not set up as iframes. If they are set up as iframes, but the games don't for another reason, this script will not list the game as broken.

## How to use it?

- List all the slugs you want to check in `slugs.xlsx`
- Run the script `main.py`
- Once the script is done running, it creates (or updates) the file `games.xlsx` listing the status of all games

## Requirements

- `pandas` (possibly `openpyxl` as well)
- `beautifulsoup4`
