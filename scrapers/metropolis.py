import requests
from bs4 import BeautifulSoup
from models import db, Event
from datetime import datetime
#print("SCRAPER STARTED")

current_year = datetime.now().year
def scrape():
    url = "https://teatrulmetropolis.ro/program/"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Request failed with status: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    events = []

    row_sections = soup.select("div.row:has(.cal-date)")
    #print("Filtered event rows:", len(row_sections))
    for row_section in row_sections:
        #print(f"Processing row section: {row_section}")
        #print(row_sections[0].prettify())
        row_section_date = row_section.find("span", class_="cal-date")  
        #print(f"Extracted date text: {row_section_date.get_text(strip=True) if row_section_date else 'No date'}")
        date_text = row_section_date.get_text(strip=True) if row_section_date else "No date"
        
        if date_text == "No date":
            continue
        
        try:
            date_obj = datetime.strptime(date_text, "%d.%m")
            date_obj = date_obj.replace(year=current_year)
            #print(f"Parsed date: {date_obj} from text: {date_text}")
        except ValueError:
            print(f"Could not parse date: {date_text}")
            continue

        title_tag = row_section.find("div", class_="cboxtitle")
        title = title_tag.text.strip() if title_tag else "No title"
        #print(f"Processing event: {title} on date: {date_obj}")
        time_tag = row_section.find("span", class_="show-ora")
        time_text = time_tag.contents[0].strip() if time_tag else None
        if time_text:
                try:
                    time_obj = datetime.strptime(time_text, "%H:%M").time()
                    date_obj = datetime.combine(date_obj.date(), time_obj)
                except ValueError:
                    print(f"Invalid time format: {time_text}")

        
        existing = Event.query.filter_by(
                title=title,
                date=date_obj,
                venue="Teatrul Metropolis"
                ).first()

        if not existing:    
                new_event = Event(
                    title=title,
                    date=date_obj,
                    venue="Teatrul Metropolis",
                    source=url,
                    type="theater"
                    #price=price_text
                )
                db.session.add(new_event)

    db.session.commit()
    #print("HTML length:", len(response.text))
    return events