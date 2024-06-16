# app/utils.py
from flask_mail import Message
from .extensions import mail
import logging

def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    try:
        mail.send(msg)
        logging.info(f'Email sent to {recipients}')
    except Exception as e:
        logging.error(f'Failed to send email to {recipients}: {e}')
