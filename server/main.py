import json
import smtplib
import os

from flask import Flask
from flask_pymongo import PyMongo
from settings import BAK_EMAIL_USERNAME, BAK_EMAIL_PASSWORD, DB_NAME

app = Flask(__name__)

with app.app_context():
    # Python mongodb configuration
    app.config['MONGO_DBNAME'] = DB_NAME
    app.config['MONGO_HOST'] = 'db'  # Mongo container hostname
    MONGO = PyMongo(app)
    USER_COLLECTION = MONGO.db.user

MAIL_SERVER = smtplib.SMTP_SSL('smtp.qq.com')
MAIL_SERVER.login(BAK_EMAIL_USERNAME, BAK_EMAIL_PASSWORD)


@app.route('/')
def index():
    """Return default page"""
    return "Server is running..."


@app.route('/subscribe', methods=['post'])
def subscribe(email, sites):
    """
  Receive form post from index page. Including email and sited are subscribed
  """
    user = USER_COLLECTION.find_one({'email': email}, {'_id': 1})
    if user is None:
        # Register an account
        USER_COLLECTION.insert_one({'email': email, 'sites': sites})
    else:
        # Update sites list
        USER_COLLECTION.update_one({
            '_id': user['_id'],
        }, {'sites': sites})


@app.route('/fetch', methods=['post'])
def fetch(items):
    items = json.loads(items)
    for item in items:
        # Find all users who subscribed this site
        users = USER_COLLECTION.find({'sites': {'$in': [item.name]}})

        # Send email to user
        for user in users:
            sendEmail(user.email, item)

    # All email sent, close email server
    MAIL_SERVER.quit()


def sendEmail(email_address, item):
    fromaddr = BAK_EMAIL_USERNAME
    toaddrs = email_address
    subject = "Test!!!"
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" %
           (fromaddr, ", ".join(toaddrs), subject))

    MAIL_SERVER.sendmail(fromaddr, toaddrs, msg)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
