from flask import Flask
from models import db, Event
from scraper import get_events
from flask import render_template

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///events.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Route to display events on the homepage. When user lands on /,do
@app.route("/")
def home():
    events = Event.query.all()
    return render_template("index.html", events=events)
# String construction of HTML output with f string literal prefix
# (no longer needed, due to render template above) 

#    output = ""
#    for event in events:
#        output += f"<h2>{event.title}</h2><p>{event.date}</p>"
#
#    return output
# Run the app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        get_events()

    app.run(debug=True)