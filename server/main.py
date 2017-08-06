import json

from pika import ConnectionParameters, BlockingConnection
from flask import Flask, request
from flask_pymongo import PyMongo
from settings import DB_NAME, DB_HOST, DEBUG, MQ_HOST, QUEUE_NAME

app = Flask(__name__)
connection = BlockingConnection(ConnectionParameters(MQ_HOST))
channel = connection.channel()

channel.queue_declare(queue=QUEUE_NAME)

with app.app_context():
    # Python mongodb configuration
    app.config['MONGO_DBNAME'] = DB_NAME
    app.config['MONGO_HOST'] = DB_HOST  # Mongo container hostname
    MONGO = PyMongo(app)
    USER_COLLECTION = MONGO.db.users

@app.route('/')
def index():
    """Return default page"""
    channel.basic_publish(
        exchange='', routing_key=QUEUE_NAME, body='Test')
    return "Server is running..."

@app.route('/subscribe', methods=['POST'])
def subscribe(email, sites):
    """Receive form post from index page. Including email and sited are subscribed"""
    user = USER_COLLECTION.find_one({'email': email}, {'_id': 1})
    if user is None:
        # Register an account
        USER_COLLECTION.insert_one({'email': email, 'sites': sites})
    else:
        # Update sites list
        USER_COLLECTION.update_one({
            '_id': user['_id'],
        }, {'sites': sites})


@app.route('/fetch', methods=['POST'])
def fetch():
    """Fetch posts from newsSpider"""
    print(request.form.get('post'))
    post = json.loads(request.form.get('post', {}))
    # Find all users who subscribed this site
    users = USER_COLLECTION.find({
        'sites': {'$in': [post['name']]}
    })
    print(users)

    # Send email to user
    for user in users:
        send_email(user['email'], post)
    return json.dumps({'msg': 'ok'}), 200, {'ContentType': 'application/json'}


def send_email(email_address, post):
    """Send a request to MQ between email server"""
    channel.basic_publish(
        exchange='', routing_key=QUEUE_NAME, body=json.dumps({
            'email': email_address,
            'post': post
        }))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
