import requests
from bs4 import BeautifulSoup
from models import db, Event
from datetime import datetime
from urllib.parse import urljoin
current_year = datetime.now().year
def scrape():
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

        date_text = date_text.replace("\xa0", " ").strip().lower()

        for ro, en in months.items():
            if ro in date_text:
                date_text = date_text.replace(ro, en.lower())

        date_text = date_text.title()  # normalize → "10 April"
        
        full_date_text = f"{date_text} {current_year}"

        formats_with_year = [
            "%A, %B %d, %Y",   # Friday, April 10, 2026
            "%a, %B %d, %Y",   # Fri, April 10, 2026
            "%d %B %Y",        # 10 April 2026
         "%a %d %B %Y",     # Fri 10 April 2026
          "%d %b %Y",        # 10 Apr 2026
        ]

        formats_without_year = [
           "%d %B",           # 10 April
           "%a %d %B",        # Fri 10 April
          "%d %b",           # 10 Apr
        ]
        
        date_obj = None

        # ✅ 1. Try parsing WITH year (no modification)
        for fmt in formats_with_year:
            try: 
                 date_obj = datetime.strptime(date_text, fmt)
                 break
            except ValueError:
                 continue

        # ✅ 2. If that fails, append year and try again
        if date_obj is None:
            full_date_text = f"{date_text} {current_year}"

            for fmt in formats_without_year:
                try:
                    date_obj = datetime.strptime(full_date_text, fmt + " %Y")
                    break
                except ValueError:
                    continue

        # ❗ Final safety check
        if date_obj is None:
            print(f"Failed parsing: '{date_text}'")
            continue

        event_blocks = date_section.find_all("div", class_="events")

        for event in event_blocks:
            title_tag = event.find("h2") or event.find("h3") or event.find("a")
            title = title_tag.text.strip() if title_tag else "No title"

            base_url = "https://www.control-club.ro"
            link = a.get("href") if (a := event.find("a")) else None
            link = urljoin(base_url, link)

            img= event.find("div", class_="img")
            img_tag = img.find("img") if img else None
            image_url= img_tag.get("src") if img_tag else None
            print("IMAGE URL:", image_url)  

            print(f"Processing event: {title} on date: {date_obj} with link: {link}")
            time_tag = event.find("span", class_="hour")
            time_text = time_tag.contents[0].strip() if time_tag else None
            if time_text:
                try:
                    time_obj = datetime.strptime(time_text, "%H:%M").time()
                    date_obj = datetime.combine(date_obj.date(), time_obj)
                except ValueError:
                    print(f"Invalid time format: {time_text}")

           #  PRICE CAN'T BE EXTRACTED BECAUSE IT IS PROBABLY JS LOADED
           #  parent = event.parent
            #price_tag = parent.select_one(".ticket-price price")
            #current = event
            #while current:
            #    price_tag = current.select_one(".ticket-price price")
           #     if price_tag:
            #        break
            #    current = current.parent
           # price_text = price_tag.get_text(strip=True) if price_tag else None
            #print("PRICE:", price_tag)
            #print("ticket-price" in response.text)

            # ✅ Save to DB HERE
            #DB PUSH

            VENUE= "Club Control"
            details=""  # no details page or description available

            from db_utils import save_event
            status = save_event(title, date_obj, VENUE, link, details, image_url, event_type="Concert")
            print(status, title)
        from db_utils import commit_events
        commit_events() 

    return events