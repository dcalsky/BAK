import smtplib
import json
from os import path
from jinja2 import Template
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pika import BlockingConnection, ConnectionParameters
from settings import BAK_EMAIL_USERNAME, BAK_EMAIL_PASSWORD, SMTP_ADDRESS, MQ_HOST, QUEUE_NAME

# Email server Initialize
MAIL_SERVER = smtplib.SMTP_SSL(SMTP_ADDRESS)
MAIL_SERVER.login(BAK_EMAIL_USERNAME, BAK_EMAIL_PASSWORD)

# MQ Initialize
connection = BlockingConnection(ConnectionParameters(host=MQ_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)


def sendEmail(email_address, post):
    fromaddr = BAK_EMAIL_USERNAME
    toaddrs = email_address
    subject = '北安跨: 同济大学%s的新闻' % (post['name'], )
    text = ''

    # TODO: Beautify mail template
    template = Template(
        open(path.join(path.dirname(__file__), './email-template.html'), 'rt').read())
    html = template.render(post=post)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    MAIL_SERVER.sendmail(fromaddr, toaddrs, msg.as_string())


def queue_callback(ch, method, properties, body):
    try:
        content = json.loads(body.decode('utf-8'))
        email = content['email']
        post = content['post']
        sendEmail(email, post)
    except json.decoder.JSONDecodeError:
        # TODO: add an alarm to avoid message queue heaps up
        print('Decode wrong')


if __name__ == '__main__':
    print('Email Server: waiting for emails ...')
    channel.basic_consume(queue_callback, queue=QUEUE_NAME)
    channel.start_consuming()
