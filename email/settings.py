import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(
    find_dotenv(
        os.path.join(
            os.path.join(os.path.dirname(__file__), os.path.pardir), '.env')))

BAK_EMAIL_USERNAME = os.environ.get('BAK_EMAIL_USERNAME',
                                    'email_sender_username')
BAK_EMAIL_PASSWORD = os.environ.get('BAK_EMAIL_PASSWORD',
                                    'email_sender_password')

SMTP_ADDRESS = 'smtp.qq.com'

MQ_HOST = 'localhost'
