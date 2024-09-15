"""
Этот файл представляет собой основной файл маршрутизации для веб-приложения на Flask.

В этом файле определяются маршруты (URL-адреса), которые соответствуют различным страницам сайта. 
Каждый маршрут связан с определенной функцией, которая вызывается при обращении к указанному адресу. 
Эти функции обычно возвращают рендеринг HTML-шаблонов, которые затем отображаются в браузере пользователя.

Что писать в этом файле:
- Определяйте новые маршруты для страниц вашего сайта с помощью декоратора @app.route('<маршрут>').
- Для каждого маршрута создавайте соответствующую функцию, которая будет обрабатывать запросы на этот маршрут.
- В функциях используйте render_template для рендеринга HTML-шаблонов (например, index.html).
- Если у вас есть закомментированные маршруты для будущих страниц, вы можете их раскомментировать и настроить для новых страниц.

Пример: 
Если вы хотите добавить страницу контактов, вы можете добавить следующий код:

@app.route('/contact')
def contact():
    return render_template('contact.html')

Таким образом, при переходе по адресу '/contact' будет отображаться страница с шаблоном 'contact.html'.
"""

from flask import render_template, request, redirect, url_for, make_response
from flask_mail import Mail, Message
from app.config import URL
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app import app
from database.DATABASE import DatabaseManager

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

def send_email2(user_email, text):
    msg = Message(
        "Ваш 4 значный код для подтверждения регистрации",
        sender="kirill.kim.0223@gmail.com",
        recipients=[user_email]
    )
    msg.body = text

    try:
        mail.send(msg)
        print(f"Письмо с кодом {text} успешно отправлено")
    except Exception as error:
        print(error)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'kirill.kim.0223@gmail.com'
app.config['MAIL_PASSWORD'] = 'xhfr xkuk lpvg nlps'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
url = URL()
db = DatabaseManager("database/USER.db")

@app.route("/home")
@app.route("/")
def index():
    logged = request.cookies.get("logged")
    user_name = request.cookies.get("user_name")
    print(user_name)
    if logged == "yes":
        reg_or_profil = "Профиль"
        url_reg_or_profil = url.profil
    else:
        reg_or_profil = "Зарегистрироваться"
        url_reg_or_profil = url.create_account

    return render_template("index.html",
                           user_name = user_name if user_name else "Гость",
                           reg_or_profil = reg_or_profil,
                           url_reg_or_profil = url_reg_or_profil
                           )


@app.route(str(url.news))
def news():
    return render_template("news.html")


@app.route(str(url.profil))
def profil():
    return render_template("profil.html",
                            user_name = request.cookies.get("user_name"),
                            email = request.cookies.get("email")
                            )


@app.route("/posts", methods=["POST", "GET"])
def posts():
    posts_content = ""
    if request.method == "POST":
        posts_content = request.form["post_content"]

    my_post = posts_content if len(posts_content) > 0 else "none"
    return render_template("posts.html", my_post = my_post)


@app.route("/out")
def out():
    res = make_response("<h1>logout</h1>")
    res.delete_cookie("logged")
    res.delete_cookie("user_name")
    res.delete_cookie("email")
    res.delete_cookie("password")
    res.delete_cookie("email_verification_sent")
    res.delete_cookie("verification_code")
    return res

@app.route(str(url.login_account), methods=["POST", "GET"])
def login_account():
    response = make_response(render_template("login_account.html"))
    logged = request.cookies.get("logged")

    if logged == "yes":
        return redirect(str(url.successful_registration))

    if request.method == "POST":
        user = {
            "name": request.form["username"],
            "password": request.form["password"],
            "email": request.form["email"]
        }

        users = db.fetch(table_name="user")

        for u in users:
            if user["name"] in u and user["password"] in u and user["email"] in u:
                print("Пользователь существует")

                response = make_response(redirect(str(url.email_verification)))
                response.set_cookie("logged", "50%")
                response.set_cookie("user_name", user["user_name"])
                response.set_cookie("email", user["email"])
                response.set_cookie("email_verification_sent", "no")
                return response
        
        response = "<h1>Ошибка: Неправильное имя пользователя или пароль</h1>"

    return response


@app.route(str(url.create_account), methods=["POST", "GET"])
def create_account():
    response = make_response(render_template("create_account.html"))
    logged = request.cookies.get("logged")

    if logged == "yes":
        return redirect(str(url.successful_registration))

    if request.method == "POST":
        user = {
            "name": request.form["username"],
            "email": request.form["email"],
            "password": request.form["password"],
            "confirm_password": request.form["confirm_password"]
        }

        if str(user["password"]) == str(user["confirm_password"]):
            try:
                db_answer = db.check_and_insert(user_name=user["name"], 
                                                password=user["password"],
                                                email=user["email"])
                if db_answer:
                    response = make_response(redirect(str(url.email_verification)))
                    response.set_cookie("logged", "50%")
                    response.set_cookie("user_name", user["name"])
                    response.set_cookie("email", user["email"])
                    response.set_cookie("email_verification_sent", "no")
                else:
                    response = make_response(f"Пользователь {user['name']} уже существует")
            except Exception as e:
                print(f"Ошибка базы данных: {e}")
                response = make_response(f"Ошибка базы данных: {e}")
        else:
            response = make_response("Пароли не совпадают")

    return response



@app.route(str(url.email_verification), methods=["POST", "GET"])
def email_verification():
    if request.cookies.get("email_verification_sent") != "yes":
        if request.cookies.get("verification_code") is None:
            really_verification_code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            send_email2(request.cookies.get("email"), really_verification_code)
            response = make_response(render_template("email_verification.html"))
            response.set_cookie("email_verification_sent", "yes")
            response.set_cookie("verification_code", str(really_verification_code))
            return response

    if request.method == "POST":
        verification_code = request.form.get("verification_code")
        print(f"________________________________ {verification_code}")
        stored_verification_code = request.cookies.get("verification_code")

        if verification_code != stored_verification_code:
            return "<h1>Неверный код подтверждения email. Повторите еще раз.</h1>"
        else:
            response = redirect(str(url.successful_registration))
            response.set_cookie("logged", "yes")
            return response

    return render_template(str(url.email_verification))



@app.route(str(url.successful_registration))
def successful_registration():
    return render_template("successful_registration.html")


@app.route(str(url.games))
def games():
    return render_template("games.html")
