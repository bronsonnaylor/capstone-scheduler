from flask import Flask, Blueprint, jsonify, request, redirect, session
from db_instance import db
from models import User, Event, Invites
from datetime import datetime
import os
import flask
from sqlalchemy.exc import IntegrityError

user_api = Blueprint('user_api', __name__)

login_info = []
passBool = ''
nameBool = ''
registerBool = ''

@user_api.route('/user', methods=['GET'])
def serve_all_users():

    try:
        user_usernames = session['test_query']
    except KeyError:
        user_usernames = session['new_user']
        print("usernames line 30    " + str(user_usernames))
    
    
    return jsonify({"usernames": user_usernames})

@user_api.route('/getevents', methods=['GET'])
def serve_all_events():
    event_instances = db.session.query(Event).all()
    # do not change the %Y-%m-%d %H:%M:%S format of these times in the line
    #  below because this is being used in that format on the calendar ** PK
    user_events = [{"id":event.id, "event_name": event.event_name, "details": event.details, "start_time": event.start_time.strftime("%Y-%m-%d %H:%M:%S"), "end_time":event.end_time.strftime("%Y-%m-%d %H:%M:%S"), "all_day": event.all_day, "owner_id":event.owner_id} for event in event_instances]
    return jsonify({"all_events": user_events})

@user_api.route('/getinvites', methods=['POST'])
def get_invites():
    event_id = request.json["event_id"]
    event_invites = Invites.query.filter_by(event_id=event_id).all()
    event_invites_array = [{'email':event_invite.invitee_email, 'accepted': event_invite.accepted} for event_invite in event_invites]
    print("eventinvitesarray line 41    " + str(event_invites_array))
    return jsonify({'all_invites': event_invites_array})

@user_api.route('/usersignup', methods=['POST'])
def add_user():
        new_user = User()
        new_user.username = request.json["new_user"]
        new_user.password = request.json["new_password"]
        new_confirm = request.json["new_pass_confirm"]
        db.session.add(new_user)

        try:

            if new_user.password != new_confirm:
                passBool = False
                registerBool = False
                nameBool = True
                
            else:
            
                passBool = True
                db.session.commit()
                nameBool = True
                registerBool = True
                session['new_user'] = new_user.id
                usernamesession = session['new_user']
                
        except IntegrityError as error:
        
            registerBool = False
            nameBool = False
        
        return jsonify(regBool=registerBool, passwordBool=passBool, newNameBool = nameBool)

@user_api.route('/newevent', methods=['POST'])
def add_event():
    new_event = Event()

    startTimeObject = datetime.strptime(request.json["event_start_time"], "%Y-%m-%d %H:%M:%S")
    endTimeObject = datetime.strptime(request.json["event_end_time"], "%Y-%m-%d %H:%M:%S")
    new_event.start_time = startTimeObject
    new_event.end_time = endTimeObject
    new_event.all_day = request.json["all_day"]
    new_event.event_name = request.json["event_name"]
    new_event.details = request.json["event_details"]
    new_event.owner_id = request.json["owner_id"]
    if new_event.owner_id != "" and new_event.event_name != "" and new_event.start_time != "":
        db.session.add(new_event)
        db.session.commit()
    return jsonify(success=True, event_id=new_event.id)

@user_api.route('/deleteevent', methods=['DELETE'])
def delete_event():
    event_id = request.json["event_id"]
    to_delete = Event.query.filter_by(id=event_id).one()
    db.session.delete(to_delete)
    db.session.commit()
    return jsonify(success=True)

@user_api.route('/user_login', methods=['POST'])
def user_login():
    
    entered_username = request.json["username_item"]
    entered_password = request.json["password_item"]
    login_info.append(entered_username)
    login_info.append(entered_password)
    
    return jsonify(success=True)

@user_api.route('/verify_login', methods=['GET'])
def verify_login():

    test_query = db.session.query(User).filter(User.username==login_info[0], 
    User.password==login_info[1]).scalar()
    
    if test_query != None:
        loginValid = True
        session['test_query'] = test_query.id
        usernamesession = session['test_query']
        login_info.clear()
    else:
        loginValid = False
        login_info.clear()

    return jsonify({"loginbool": loginValid})

@user_api.route('/checksession', methods=["GET"])
def check_session():
    
    if 'test_query' in session:

        return jsonify(
                session = True,
                user = session['test_query'] 
                )
    elif 'new_user' in session:
        
        return jsonify(
                session = True,
                user = session['new_user'] 
                )
        
    else:
        
        return jsonify(session = False)

@user_api.route("/logout", methods=["GET"])
def logout():

    if 'test_query' in session:
        del session['test_query']

        return jsonify(success=True)

    else:
        del session['new_user']

        return jsonify(success=True)

