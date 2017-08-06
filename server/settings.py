import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env'))

DB_NAME = 'BAK'
DB_HOST = 'db'
MQ_HOST = 'mq'
QUEUE_NAME = 'post'

DEBUG = os.environ.get('DEBUG', 0)
