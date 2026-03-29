import requests
from bs4 import BeautifulSoup
from models import db, Event

def get_events():
    url = "https://www.control-club.ro/events/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Request failed with status: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    events = []

    date_sections = soup.find_all("div", class_="date")

    for date_section in date_sections:
        date_section_title = date_section.find("div", class_="title")    

        date_text = date_section_title.get_text(strip=True) if date_section_title else "No date"

        event_blocks = date_section.find_all("div", class_="events")

        for event in event_blocks:
            title_tag = event.find("h2") or event.find("h3") or event.find("a")
            title = title_tag.text.strip() if title_tag else "No title"

            # ✅ Save to DB HERE
            new_event = Event(
                title=title,
                date=date_text,
                venue="Control Club",
                source=url
            )

            db.session.add(new_event)

            # still keep list if you want
            events.append({
                "title": title,
                "date": date_text
            })

    # ✅ Commit ONCE (important!)
    db.session.commit()

    return events