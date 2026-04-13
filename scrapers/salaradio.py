from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
import re
from calendar import month
#import requests
from bs4 import BeautifulSoup
from models import db, Event
from datetime import datetime

VENUE = "Sala Radio"

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # optional (enable later if needed)

    driver_path = ChromeDriverManager().install()
    # fix wrong file selection (KEEP THIS)
    if "THIRD_PARTY" in driver_path:
        driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")

    driver = webdriver.Chrome(
        service=Service(driver_path),
        options=options
    )

    return driver


def scrape():
    print("Scraper started...")  # optional debug
    events = []
    try:
        driver = get_driver()

        url = "https://salaradio.ro/evenimente/"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "h3.ex-h1 a")
            )
        )

        links = []
        for a in driver.find_elements(By.CSS_SELECTOR, "h3.ex-h1 a"):
            href = a.get_attribute("href")
            links.append(href)
        
        print("Found links:", len(links))
        for link in links:
            driver.get(link)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.em-event-content")))
            #content = driver.find_element(By.CSS_SELECTOR, "section.em-event-content").text
            #print(content[:300])
            
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            title_tag = soup.select_one("h1.title")
            title = title_tag.get_text(strip=True) if title_tag else "No title"
            print("TITLE:", title)
            

            date_tag = soup.select_one(".em-event-date")
            time_tag = soup.select_one(".em-event-time")

            date_text = date_tag.get_text(strip=True) if date_tag else ""
            time_text = time_tag.get_text(strip=True) if time_tag else ""

            # extract start time
            start_time = time_text.split(" - ")[0] if time_text else ""

            # parse
            date_obj = datetime.strptime(date_text, "%d/%m/%Y")
            time_obj = datetime.strptime(start_time, "%I:%M %p")

            datetime_str = f"{date_obj.strftime('%Y-%m-%d')} {time_obj.strftime('%H:%M')}"
            try:
                date_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                print("PARSED:", date_obj)
            except Exception as e:
                #print("Failed parsing:", full_text, e)
                continue

            import re

            details_tag = soup.select_one("section.em-event-content")

            if details_tag:
                details = details_tag.get_text(separator="\n", strip=True)

                # remove date line
                details = re.sub(
                    r"^(Luni|Marți|Miercuri|Joi|Vineri|Sâmbătă|Duminică).*?\d{4}.*\n?",
                    "",
                    details,
                    flags=re.MULTILINE
                )

                # remove junk
                details = details.replace("PrintFriendly", "")

                # minimal fixes
                details = re.sub(r"\n([–\-])", r" \1", details)
                details = re.sub(r":\n+", ": ", details)

                # clean spacing
                details = re.sub(r"\n\s*\n+", "\n\n", details).strip()
                # fix punctuation broken by tags
                details = re.sub(r"\n([,.:])", r"\1", details)

                # fix dash lines
                details = re.sub(r"\n([–\-])", r" \1", details)

                # fix lowercase continuation (e.g. "pentru pian...")
                details = re.sub(r"\n([a-zăâîșț])", r" \1", details)
            else:
                details = ""

            print(details)
            
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
                        type="Concert",
                        details=details
                        #price=price_text
                    )  
                    db.session.add(new_event)
                    #events.append(new_event)

        db.session.commit()
        
    finally:
        driver.quit()
    
    return events
    #return 1

if __name__ == "__main__":
    events = scrape()
    #for event in events:
        #print(event.title, event.date, event.venue) 