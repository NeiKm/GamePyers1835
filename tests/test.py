import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'nei.km.0223@gmail.com' 
smtp_password = '####'      

msg = MIMEMultipart()
msg['From'] = smtp_username
msg['To'] = 'kiryha.pro.0223@gmail.com'
msg['Subject'] = 'Тестовое письмо от Python'


body = 'Это тестовое письмо, отправленное из Python'
msg.attach(MIMEText(body, 'plain'))


try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.send_message(msg)
    print('Email отправлен успешно!')
except Exception as e:
    print(f'Ошибка при отправке email: {e}')
finally:
    server.quit()
