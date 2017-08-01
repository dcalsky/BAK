import json
import smtplib
from flask import Flask
from flask_pymongo import PyMongo
from .setting import BAK_EMAIL_USERNAME, BAK_EMAIL_PASSWORD

__name__ = 'BAK'

app = Flask(__name__)
MONGO = PyMongo(app)
USER_COLLECTION = MONGO.db.user
flake8 = smtplib.SMTP_SSL('smtp.qq.com')
flake8.login(BAK_EMAIL_USERNAME, BAK_EMAIL_PASSWORD)


@app.route('/')
def index():
  """Return default page"""
  return 'Flask'


@app.route('/subscribe', methods=['post'])
def subscribe(email, sites):
  """Receive form post from index page. Including email and sited are subscribed"""
  user = USER_COLLECTION.find_one({'email': email})
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
  flake8.quit()


def sendEmail(email, item):
  fromaddr = ""
  toaddrs = ""
  subject = ""
  msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" %
         (fromaddr, ", ".join(toaddrs), subject))

  # server.set_debuglevel(1)

  flake8.sendmail(fromaddr, toaddrs, msg)
