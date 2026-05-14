from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from calendar import month
#import requests
from bs4 import BeautifulSoup
from db_utils import commit_events, save_event
from models import db, Event
from datetime import datetime


VENUE = "Ateneul Roman"
from selenium.webdriver.common.by import By
def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # optional (enable later if needed)

    driver_path = ChromeDriverManager().install()
    # fix wrong file selection (KEEP THIS)
    if "THIRD_PARTY" in driver_path:
        driver_path = os.path.join(os.path.dirname(driver_path), "chromedriver.exe")

    # DEBUG (no longer needed)
    # print("FINAL DRIVER PATH:", driver_path)

    driver = webdriver.Chrome(
        service=Service(driver_path),
        options=options
    )

    return driver


def scrape():
    # print("Scraper started...")  # optional debug
    events = []
    try:
        driver = get_driver()

        url = "https://filarmonicaenescu.ro/ro/evenimente"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'a[href^="/ro/eveniment/"]')
            )
        )

        # print(driver.page_source[:1000])
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        articles = soup.find_all("article")
        
        links = []
        #print("LINKS TYPE:", type(links))
        #print("print is:", print)
        #print("append is:", links.append)
        for article in articles:
            a_tag = article.find("a")

            if not a_tag:
                continue

            link = a_tag.get("href")

            if not link:
                continue

            # ❌ EXCLUDE festival events
            if "/ro/eveniment/" not in link:
                #print("SKIPPED:", link)
                continue

            # ✅ KEEP others
            links.append(link)
            #print("VALID:", link)
        
        #build absolute URLs
        base = "https://filarmonicaenescu.ro"

        for link in links:
            if link.startswith("/"):
                link = base + link
            #print("OPENING:", link)

            driver.get(link)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.hidden > div")))

            detail_html = driver.page_source
            detail_soup = BeautifulSoup(detail_html, "html.parser")

            #title
            title_tag = detail_soup.select_one("section > h2")
            title = title_tag.get_text(strip=True) if title_tag else "No title"
            
            #date
            #print(detail_soup.select("div.hidden"))
            first_block = detail_soup.select_one("div.hidden > div")

            date_parts = first_block.find_all("p") if first_block else []

            
            day = date_parts[1].get_text(strip=True) if len(date_parts) > 1 else None
            month = date_parts[2].get_text(strip=True) if len(date_parts) > 2 else None
            #date_text = f"{day} {month}"    

            # time
            time_tags = detail_soup.select("div.hidden.lg\\:flex time")
            time_text = time_tags[0].get_text(strip=True) if time_tags else "00:00"

            # combine
            datetime_text = f"{day} {month} 2026 {time_text}"
            
            #print(datetime_text)
            
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

            full_text = f"{day} {month_en} 2026 {time_text}"

            try:
                date_obj = datetime.strptime(full_text, "%d %B %Y %H:%M")
                #print("PARSED:", date_obj)
            except Exception as e:
                #print("Failed parsing:", full_text, e)
                continue

            details_tag = detail_soup.select_one("section > div:nth-of-type(3) > div:nth-of-type(2)")

            if details_tag:
                elements = details_tag.select("p, h4")
                
                lines = []
                for el in elements:
                    text = el.get_text(separator=" ", strip=True)
                    if not text:
                        continue
                    
                    if el.name == "h4" and lines:
                        lines.append("")  
                        continue
                    else:
                        lines.append(text)

                details = "\n".join(lines).strip()
            else:
                details = ""
                #details = details.replace("\nProgram", "")  # add extra newline and no "Program"

            #print("DETAILS:", details)
            #images
            img_tag = detail_soup.select_one('meta[property="og:image"]')
            image_url = img_tag.get("content") if img_tag else None
            print("IMAGE URL:", image_url)
            
            #DB PUSH
            status = save_event(title, date_obj, VENUE, link, details, image_url, event_type="Concert")
            print(status, title)
        commit_events() 

    finally:
        driver.quit()
    
    return events


if __name__ == "__main__":
    events = scrape()
    #for event in events:
        #print(event.title, event.date, event.venue) 