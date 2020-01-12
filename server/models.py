from db_instance import db
# from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(500))

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(500), nullable=False)
    details = db.Column(db.String(2000))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    all_day = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # shared_ids = db.Column(db.Integer, db.ForeignKey("user.id"))

class Invites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invitee_email = db.Column(db.String(500))
    accepted = db.Column(db.Boolean, default=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"))