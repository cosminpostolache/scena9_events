import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

from db_utils import save_event, commit_events

VENUE = "Expirat"

def scrape():
    url = "https://zilesinopti.ro/locuri/expirat-halele-carol/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed request:", response.status_code)
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    print(response.text[:1000])  # Debug print to check HTML structure

    current_year = datetime.now().year
    items = soup.select("div.kzn-sw-item")

    for item in items:
        # --- TITLE + LINK ---
        title_tag = item.select_one("h3 a")
        if not title_tag:
            continue

        raw_title = title_tag.get_text(strip=True)
        link = title_tag.get("href")

        # clean title (remove "@ Expirat" etc.)
        title = re.split(r"\s*@\s*", raw_title)[0]

        # --- DATE ---
        date_div = item.select_one(".kzn-one-event-date div:first-child")
        date_text = date_div.get_text(strip=True) if date_div else ""

        match_date = re.search(r"(\d{2}/\d{2})", date_text)

        # --- TIME ---
        time_div = item.select_one(".kzn-one-event-date div:nth-child(2)")
        time_text = time_div.get_text(strip=True) if time_div else ""

        if not match_date or not time_text:
            continue

        try:
            date_obj = datetime.strptime(
                f"{match_date.group(1)}/{current_year} {time_text}",
                "%d/%m/%Y %H:%M"
            )
        except Exception as e:
            print("Failed parsing:", raw_title, e)
            continue

        # --- DETAILS ---
        summary_tag = item.select_one(".kzn-sw-item-sumar")
        details = summary_tag.get_text(strip=True) if summary_tag else ""

        # --- DB SAVE ---
        status = save_event(title, date_obj, VENUE, link, details)
        print(status, title)

    commit_events()

    return []