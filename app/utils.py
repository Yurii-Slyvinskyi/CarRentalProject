from smtplib import SMTPException

from . import mail, db
from flask import render_template, current_app, flash, redirect, url_for
from threading import Thread
from flask_mail import Message


def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipient, template, **kwargs):
        app = current_app._get_current_object()
        msg = Message(subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[recipient])
        msg.html = render_template(template, **kwargs)
        thr = Thread(target=async_send_mail, args=(app, msg))
        thr.start()
        return thr
