#from asyncio import events

from flask import Flask
from models import db, Event
from scraper import get_events
from flask import render_template
from collections import defaultdict
from datetime import date, timedelta

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Route to display events on the homepage. When user lands on /,do
@app.route("/")
def home():
    events = Event.query.order_by(Event.date).all()
    #for e in events:
     #  print(e.title, e.date, e.venue)
    #print("TOTAL EVENTS:", len(events))
    
    grouped_events = defaultdict(list)
    for event in events:
        date_key = event.date.date()
        grouped_events[date_key].append(event)
    #for date, evs in grouped_events.items():
     #   print("DATE:", date)
      #  print("TYPE:", type(evs))
       # print("CONTENT:", evs)
        #print("COUNT:", len(evs))
    grouped_events = dict(sorted(grouped_events.items()))
    today = date.today()
    return render_template(
        "index.html", 
        grouped_events=grouped_events,
        today=today,
        timedelta=timedelta)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        get_events()

    app.run(debug=True, use_reloader=False)