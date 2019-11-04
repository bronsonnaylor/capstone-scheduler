from flask import Blueprint, jsonify, request
from db_instance import db
from models import User, Event
from datetime import datetime

user_api = Blueprint('user_api', __name__)

@user_api.route('/user', methods=['GET'])
def serve_all_users():
    user_instances = db.session.query(User).all()
    user_usernames = [{"id": user.id, "username": user.username} for user in user_instances]
    return jsonify({"usernames": user_usernames})

@user_api.route('/getevents', methods=['GET'])
def serve_all_events():
    event_instances = db.session.query(Event).all()
    user_events = [{"event_name": event.event_name, "details": event.details, "datetime": event.start_time, "owner_id":event.owner_id} for event in event_instances]
    return jsonify({"all_events": user_events})

@user_api.route('/usersignup', methods=['POST'])
def add_user():
    new_user = User()
    new_user.username = request.json["new_user"]
    db.session.add(new_user)
    db.session.commit()
    return jsonify(success=True)

@user_api.route('/newevent', methods=['POST'])
def add_event():
    new_event = Event()
    
    startTimeObject = datetime.strptime(request.json["event_start_time"], "%Y-%m-%d %H:%M:%S")
    new_event.start_time = startTimeObject
    # new_event.start_time = request.json["event_start_time"]
    new_event.event_name = request.json["event_name"]
    new_event.details = request.json["event_details"]
    new_event.owner_id = request.json["owner_id"]
    # if new_event.end_time != "":
    #     new_event.end_time = request.json["event_end_time"]
    if new_event.owner_id != "" and new_event.event_name != "" and new_event.start_time != "":
        db.session.add(new_event)
        db.session.commit()
    return jsonify(success=True)