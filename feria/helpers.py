from flask_mail import Message
from feria.extensions import mail

def send_email(subject, recipient, body):
    msg = Message(subject, sender="facuvulcano1999@gmail.com", recipients=[recipient])
    msg.body = body
    mail.send(msg)