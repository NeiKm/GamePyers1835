from flask import render_template, request, redirect, url_for, make_response
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(text, user_email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg["From"] = "kirill.kim.0223@gmail.com"
    msg["To"] = user_email
    msg["Subject"] = "Ваш 4 значный код для подтверждения регистрации"

    msg.attach(MIMEText(text, "plain"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login("kirill.kim.0223@gmail.com", "xhfr xkuk lpvg nlps")

        server.sendmail("kirill.kim.0223@gmail.com", user_email, msg.as_string())
        server.quit
        print(f"Письмо {text} успешно отправлено")

    except Exception as error:
        print(error)

send_email(text="hi", user_email="kiryha.pro.0223@gmail.com")
