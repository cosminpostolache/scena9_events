from calendar import month
import requests
from bs4 import BeautifulSoup
from models import db, Event
from datetime import datetime
#print("SCRAPER STARTED")

current_year = datetime.now().year
def scrape():
    url = "https://filarmonicaenescu.ro/ro/evenimente"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    print("Recital" in response.text)
    print(response.text[:100000])
    print(response.text.count("<article"))
    if response.status_code != 200:
        print(f"Request failed with status: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    print(len(soup.find_all("article")))
    for tag in soup.find_all(True):
        if tag.name == "article":
            print("FOUND ARTICLE")

    events = []

    articles = []

    for article in soup.select("article"):
        parent_section = article.find_parent("section")
        #print("PARENT:", parent_section)
        # if no section → keep it (important!)
        if parent_section:
            classes = parent_section.get("class") or []
            if "bg-storm" in classes:
                print("Skipping bg-storm section")
                continue

        articles.append(article)
    print("VALID ARTICLES:", len(articles)) 
    for article in articles:
    
        link_tag = article.find("a", href=True)
        if link_tag:
            link = link_tag["href"]
            print(link)
        response = requests.get(link, headers=headers)
        if response.status_code != 200:
            print(f"Request failed with status: {response.status_code}")
            continue
        detail_soup = BeautifulSoup(response.text, "html.parser")
        
        #title
        title_tag = detail_soup.select_one("section > h2")
        title = title_tag.get_text(strip=True) if title_tag else "No title"
        
        #date
        first_block = detail_soup.select_one("div.hidden.lg\\:flex > div")

        date_parts = first_block.find_all("p")

        day = date_parts[1].get_text(strip=True)
        month = date_parts[2].get_text(strip=True)
        date_text = f"{day} {month}"    

        # time
        time_tags = detail_soup.select("div.hidden.lg\\:flex time")
        time_text = time_tags[0].get_text(strip=True) if time_tags else "00:00"

        # combine
        datetime_text = f"{day} {month} 2026 {time_text}"
        
        print(datetime_text)
        
        months = {
            "ianuarie": "January",
            "februarie": "February",
            "martie": "March",
            "aprilie": "April",
            "mai": "May",
            "iunie": "June",
            "iulie": "July",
            "august": "August",
            "septembrie": "September",
            "octombrie": "October",
            "noiembrie": "November",
            "decembrie": "December"
        }

        month_en = months.get(month.lower(), month)
        full_date = f"{day} {month_en} 2026"  # or dynamic year
        date_obj = datetime.strptime(full_date, "%d %B %Y")
        
        for i, p in enumerate(date_parts):
            print(i, p.get_text(strip=True))

        month_en = months.get(month.lower(), month)
        full_text = f"{day} {month_en} 2026 {time_text}"
        date_obj = datetime.strptime(full_text, "%d %B %Y %H:%M")

        date_text = date_obj.get_text(strip=True) if date_text else "No date"
        
        if date_text == "No date":
            continue
        
        try:
            date_obj = datetime.strptime(date_text, "%d.%m")
            date_obj = date_obj.replace(year=current_year)
            #print(f"Parsed date: {date_obj} from text: {date_text}")
        except ValueError:
            print(f"Could not parse date: {date_text}")
            continue

        VENUE = "Ateneul Roman"
        
        existing = Event.query.filter_by(
                title=title,
                date=date_obj,
                venue=VENUE
                ).first()

        if not existing:    
                new_event = Event(  
                    title=title,
                    date=date_obj,
                    venue=VENUE,
                    source=link,
                    type="Concert"
                    #price=price_text
                )  
                db.session.add(new_event)

    db.session.commit()
    #print("HTML length:", len(response.text))
    return events