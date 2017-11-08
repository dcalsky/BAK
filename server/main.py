import json
import re
import dicttoxml

from pika import ConnectionParameters, BlockingConnection
from flask import Flask, request, render_template, url_for
from flask_pymongo import PyMongo
from bson.json_util import dumps
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
    POST_COLLECTION = MONGO.db.posts


@app.route('/sites', methods=['GET'])
def get_sites():
    """
    Get current available sites
    """
    sites = POST_COLLECTION.distinct( "cname" )
    return dumps({
        'sites': sites
    }), 200, {'Content-Type': 'application/json'}


@app.route('/sites/xml', methods=['GET'])
def get_sites_xml():
    """
    Get current available sites
    """
    sites = POST_COLLECTION.distinct( "cname" )
    xml = dicttoxml.dicttoxml(sites)
    return xml, 200, {'Content-Type': 'text/xml'}


@app.route('/posts', methods=['GET'])
def get_posts():
    """
    Query posts from the single site
    """
    site = request.args.get('site')
    posts = POST_COLLECTION.find({'cname': site})
    return dumps({
        'posts': posts
    }), 200, {'Content-Type': 'application/json'}


@app.route('/subscribe', methods=['POST'])
def subscribe():
    """
    Receive form post from index page. Including email and sited are subscribed
    """
    email = request.json.get('email', None)
    sites = request.json.get('sites', [])
    print(email, sites)
    email_pattern = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?"
    if email is None or re.match(email_pattern, email) is None:
        return json.dumps({'msg': 'unsupported email format'}), 400, {'ContentType': 'application/json'}

    user = USER_COLLECTION.find_one({'email': email}, {'_id': 1})
    if user is None:
        # Register an account
        USER_COLLECTION.insert_one({'email': email, 'sites': sites})
    else:
        # Update sites list
        USER_COLLECTION.update_one({
            '_id': user['_id'],
        }, {'$set': {'sites': sites}})
    return json.dumps({'msg': 'ok'}), 200, {'Content-Type': 'application/json'}


@app.route('/fetch', methods=['POST'])
def fetch():
    """Fetch posts from newsSpider"""
    post = json.loads(request.form.get('post', {}))
    # Find all users who subscribed this site
    users = USER_COLLECTION.find({
        'sites': {'$in': [post['name']]}
    })
    # Send email to users
    for user in users:
        send_email(user['email'], post)
    return json.dumps({'msg': 'ok'}), 200, {'Content-Type': 'application/json'}


def send_email(email_address, post):
    """Send a request to MQ between email server"""
    channel.basic_publish(
        exchange='', routing_key=QUEUE_NAME, body=json.dumps({
            'email': email_address,
            'post': post
        }))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
