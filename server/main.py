from flask import Flask
from flask_pymongo import PyMongo
from .setting import BAK_EMAIL_USERNAME, BAK_EMAIL_PASSWORD
import smtplib
import json

__name__ = 'BAK'

app = Flask(__name__)
mongo = PyMongo(app)
email_server = smtplib.SMTP_SSL('smtp.qq.com')
email_server.login(BAK_EMAIL_USERNAME, BAK_EMAIL_PASSWORD)

user_collection = mongo.db.user


@app.route('/')
def index():
    post = {
        'title': 'cc',
        'val': 123
    }
    mongo.db.posts.insert_one(post)
    return 'Flask！！！'


@app.route('/subscribe', methods=['post'])
def subscribe(email, sites):
    user = user_collection.find_one({
        'email': email
    })
    if user is None:
        # Register an account
        user_collection.insert_one({
            'email': email,
            'sites': sites
        })
    else:
        # Update sites list
        user_collection.update_one({
            '_id': user['_id'],
        }, {
            'sites': sites
        })


@app.route('/fetch', methods=['post'])
def fetch(items):
    items = json.loads(items)
    for item in items:
        # Find all users who subscribed this site
        users = user_collection.find({
            'sites': {
                '$in': [item.name]
            }
        })

        # Send email to user
        for user in users:
            sendEmail(user.email, item)

    # All email sent, close email server
    email_server.quit()


def sendEmail(email, item):
    fromaddr = ""
    toaddrs = ""
    subject = ""
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
           % (fromaddr, ", ".join(toaddrs), subject))

    # server.set_debuglevel(1)

    email_server.sendmail(fromaddr, toaddrs, msg)
