import json
import os.path
import urllib.request

import pandas as pd
from bs4 import BeautifulSoup


def check_game(slug, language="EN"):
    print(f"Checking {slug}/{language}")
    result = {"slug": slug, "language": language}
    with urllib.request.urlopen(f"https://onlineslotcasino.com/slots/{slug}/{language}") as response:
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        result["title"] = soup.find("title").text
        iframe = soup.find("iframe")
        if iframe is None:
            result["broken"] = True
            return result
        result["broken"] = False
        result["src"] = iframe["src"]
        return result


def check_slugs(slugs, language="EN", re_check_previously_checked_games=False):
    result = []
    if os.path.exists("games.json"):
        with open('games.json', 'r') as file:
            result = json.load(file)
    for slug in slugs[:5]:
        try:
            processed_slugs = [r["slug"] + "/" + r["language"] for r in result]
            if (slug + "/" + language in processed_slugs):
                if not re_check_previously_checked_games:
                    print(f"Game {slug}, language {language} already checked. Not re-checking.")
                    continue
                result = [r for r in result if (r["slug"] != slug and r["language"] != language)]

            result.append(check_game(slug, language=language))
            with open("games.json", "w") as file:
                file.write(json.dumps(result, indent=4))
        except Exception as e:
            print(e)


def create_xls(filename="games.json"):
    print("Creating Excel File")
    pd.read_json(filename).to_excel("games.xlsx")


def load_slugs(filename="slugs.xlsx"):
    df = pd.read_excel('slugs.xlsx')
    return df.iloc[:, 0].tolist()


if __name__ == "__main__":
    slugs = load_slugs()
    for language in ["EN"]:
        check_slugs(slugs, language=language, re_check_previously_checked_games=False)
    create_xls()
