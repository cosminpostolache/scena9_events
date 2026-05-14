from scrapers import clubcontrol
from scrapers import metropolis
from scrapers import ateneu
from scrapers import salaradio
from scrapers import expirat
from models import db 

SCRAPERS = [
    clubcontrol.scrape,
    metropolis.scrape,
    #ateneu.scrape,
    #salaradio.scrape
    #expirat.scrape
]

def get_events():
    all_events = []

    for scraper in SCRAPERS:
        all_events.extend(scraper())

    db.session.commit()

    return all_events