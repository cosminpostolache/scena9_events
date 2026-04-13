from scrapers import clubcontrol, metropolis, ateneu, salaradio
from models import db 

SCRAPERS = [
    clubcontrol.scrape,
    metropolis.scrape,
    ateneu.scrape,
    salaradio.scrape
]

def get_events():
    all_events = []

    for scraper in SCRAPERS:
        all_events.extend(scraper())

    db.session.commit()

    return all_events