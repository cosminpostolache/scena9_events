from urllib import response

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import time
from calendar import month
import json
import requests
from bs4 import BeautifulSoup
from db_utils import commit_events, save_event
from models import db, Event
from datetime import datetime


VENUE = "Muzeul Național de Artă Contemporană"
url= "https://www.mnac.ro/home"
def scrape():
    response = requests.get(url)
    print("STATUS:", response.status_code)
    print("CONTENT-TYPE:", response.headers.get("content-type"))
    print(response.text[:2000])

    return []

if __name__ == "__main__":
    events = scrape()
    #for event in events:
        #print(event.title, event.date, event.venue) 
    