# utils/db_utils.py

from database import db
from models import Event


def save_event(title, date_obj, venue, link, details, event_type="Concert"):
    existing = Event.query.filter_by(
        title=title,
        date=date_obj,
        venue=venue
    ).first()

    if existing:
        existing.details = details
        existing.source = link
        return "updated"
    
    new_event = Event(
        title=title,
        date=date_obj,
        venue=venue,
        source=link,
        type=event_type,
        details=details
    )

    db.session.add(new_event)
    return "added"


def commit_events():
    db.session.commit()