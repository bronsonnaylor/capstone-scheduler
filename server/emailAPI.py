from flask import Blueprint, jsonify, request, render_template
from db_instance import db
from models import Invites, Event
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from secrets import gmail_pass

email_api = Blueprint('email_api', __name__)
gmail_user = 'pkurjanowicz10@gmail.com'
gmail_password = gmail_pass

@email_api.route('/sendinvites', methods=['POST'])
def sendinvites():
    emails = request.json["emails"]
    event_id = request.json['event_id']
    custom_message = request.json['custom_message']
    if emails != '':
        for email in emails:
            # Add to DB
            new_invite = Invites(invitee_email=email,event_id=event_id)
            db.session.add(new_invite)
            db.session.commit()
            #send emails
            msg = MIMEMultipart()
            msg['From'] = gmail_user
            msg['To'] = email
            msg['Subject'] = 'Please accept this invite to my event!'
            # Create the body of the message (a plain-text and an HTML version).
            # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
            html = """\
            <html>
            <head></head>
            <body>
                <p>Hi!</p>
                <p> Please let me know if you will attend my event!!</p>
                <p><em> {} </em></p>
                <p><a href='http://127.0.0.1:5000/response?event_id={}&email={}&response=True'><button>Click here to accept</button></a>
                <button>Click here to reject</button></p>
            </body>
            </html>
            """.format(custom_message,event_id,email)

            # Record the MIME types of both parts - text/plain and text/html.
            # part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            # msg.attach(part1)
            msg.attach(part2)
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user,email,msg.as_string())
            server.close()
            print('Success!')
        return jsonify(success=True)

@email_api.route('/response', methods=['GET'])
def responded_to_email():
    response = request.args.get('response')
    event_id = request.args.get('event_id')
    email = request.args.get('email')
    find_invite = Invites.query.filter_by(invitee_email=email).filter_by(event_id=event_id).first()
    current_accepted_value = find_invite.accepted
    if current_accepted_value == False and response == 'True':
        update_invite = find_invite.accepted = True
        db.session.commit()
    return render_template('response.html')

@email_api.route('/eventchanged', methods=['POST'])
def event_changed():
    id = request.json["id"]
    end_time = request.json["end_time"]
    start_time = request.json["start_time"]
    event = Event.query.filter_by(id=id).first()
    event_name = event.event_name
    if event.all_day == True:
        end_time = end_time[:10]
        start_time = start_time[:10]
    else:
        end_time = end_time + ' GMT'
        start_time = start_time + ' GMT'
    invite_emails = Invites.query.filter_by(event_id=id).all()
    emails_list = []
    for email in invite_emails:
        if email.accepted == True:
            emails_list.append(email.invitee_email)
    for email in emails_list:
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = email
        msg['Subject'] = '{} has updated the event time'.format(event_name)
        # Create the body of the message (a plain-text and an HTML version).
        # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
        html = """\
        <html>
        <head></head>
        <body>
            <p>Hi!</p>
            <p>The event you are attending called {} has changed the times, here are the new times:</p>
            <p>Start Time: {}</p>
            <p>End Time: {}</p>
        </body>
        </html>
        """.format(event_name,start_time,end_time)

        part2 = MIMEText(html, 'html')

        msg.attach(part2)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user,email,msg.as_string())
        server.close()
    return jsonify(success=True)