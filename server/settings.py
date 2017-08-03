import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(os.path.join(os.path.join(os.path.dirname(__file__), os.path.pardir), '.env')))

DB_NAME = 'BAK'
DB_HOST = 'db'
DEBUG = os.environ.get('DEBUG', 0)
