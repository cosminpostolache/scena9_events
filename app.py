from flask import Flask, render_template
from scraper import get_events

app = Flask(__name__)

@app.route("/")
def home():
    events = get_events()
    return render_template("index.html", events=events)

if __name__ == "__main__":
    app.run(debug=True)