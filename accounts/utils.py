import smtplib
from email.mime.text import MIMEText
import random


def send_email(recipients):
    code = random.randint(1000, 9999)
    subject = "email confirmation"
    body = f"email code {code}"
    sender = "email"
    password = "password"

    msg = MIMEText(body)
    msg['Subject'] = subject.encode('utf-8')
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())

    return code


