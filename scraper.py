import requests
from bs4 import BeautifulSoup

"""def get_events():
    url = "https://example.com/events"  # we'll replace this later
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    events = []

    # Example structure (we will adapt to a real site later)
    for event in soup.find_all("div", class_="event"):
        title = event.find("h2").text.strip()
        date = event.find("span", class_="date").text.strip()

        events.append({
            "title": title,
            "date": date
        })

    return events"""

"""def get_events():
    return [
        {"title": "Concert A", "date": "2026-04-01"},
        {"title": "Festival B", "date": "2026-04-05"},
        {"title": "DJ Night", "date": "2026-04-10"},
    ]
"""
import requests
from bs4 import BeautifulSoup
"""
def get_events():
    url = "https://www.control-club.ro/events/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    events = []

    # 🔍 You MUST adjust selectors after inspecting HTML
    event_blocks = soup.find_all("div", class_= "events")

    for event in event_blocks:
        title_tag = event.find('a', class_='title hover')
        date_tag = event.find("div", class_='title')

        title = title_tag.text.strip() if title_tag else "No title"
        date = date_tag.text.strip() if date_tag else "No date"

        events.append({
            "title": title,
        })

    return events"""
    

import requests
from bs4 import BeautifulSoup

def get_events():
    url = "https://www.control-club.ro/events/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    events = []

    # Find all date sections
    date_sections = soup.find_all("div", class_="date")

    for date_section in date_sections:
        # Extract the date text
        date_text = date_section.get_text(strip=True)

        # Find events inside this date section
        event_blocks = date_section.find_all("div", class_="events")

        for event in event_blocks:
            title_tag = event.find("h2") or event.find("h3") or event.find("a")

            title = title_tag.text.strip() if title_tag else "No title"

            events.append({
                "title": title,
                "date": date_text
            })

    return events