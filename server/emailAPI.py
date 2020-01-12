from flask import Blueprint, jsonify, request, render_template
from db_instance import db
from models import Invites
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email_api = Blueprint('email_api', __name__)
gmail_user = 'pkurjanowicz10@gmail.com'
gmail_password = 'AtYoqLFPDQpTfrpWKT.zLP*4FU'

@email_api.route('/sendinvites', methods=['POST'])
def sendinvites():
    emails = request.json["emails"]
    print("emails line 15    " + str(emails))
    event_id = request.json['event_id']
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
                <p>Hi!<br>
                How are you?<br>
                <a href='http://127.0.0.1:5000/response?event_id={}&email={}&response=True'><button>Click here to accept</button></a>
                <button>Click here to reject</button>
                </p>
            </body>
            </html>
            """.format(event_id,email)

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

