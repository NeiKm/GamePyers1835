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
from app.config import URL
import random
from app import app
from database.DATABASE import DatabaseManager

url = URL()
db = DatabaseManager("database/USER.db")

@app.route("/home")
@app.route("/")
def index():
    logged = request.cookies.get("logged")
    user_name = request.cookies.get("user_name")
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
    res = make_response("logout")
    res.delete_cookie("logged")
    res.delete_cookie("user_name")
    res.delete_cookie("email")
    res.delete_cookie("password")
    return res

@app.route(str(url.login_account), methods=["POST", "GET"])
def login_account():
    response = make_response(render_template("login_account.html"))
    logged = request.cookies.get("logged")

    # Если уже залогинен, перенаправляем на страницу профиля
    if logged == "yes":
        return redirect(str(url.successful_registration))

    # Обработка POST запроса (попытка авторизации)
    if request.method == "POST":
        user = {
            "name": request.form["username"],
            "password": request.form["password"],
            "email": request.form["email"]
        }

        # Получаем всех пользователей из базы данных
        users = db.fetch(table_name="user")

        # Поиск пользователя в базе данных
        for u in users:
            if user["name"] in u and user["password"] in u and user["email"] in u:
                print("Пользователь существует!")

                # Если пользователь найден, сохраняем статус логина и имя в куки
                response = make_response(redirect(str(url.successful_registration)))
                response.set_cookie("logged", "yes")
                response.set_cookie("user_name", user["name"])
                response.set_cookie("email", user["email"])
                return response
        
        # Если пользователь не найден, выводим сообщение об ошибке
        return "Ошибка: Неправильное имя пользователя или пароль"

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
        print(user["confirm_password"])
        
        if str(user["password"]) == str(user["confirm_password"]):
            try:
                db_answer = db.check_and_insert(user_name=user["name"], 
                                                password=user["password"],
                                                email=user["email"])
                if db_answer:
                    response = make_response(redirect(str(url.successful_registration)))
                    response.set_cookie("logged", "yes")
                    response.set_cookie("username", user["name"])
                    response.set_cookie("email", user["email"])
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
    if request.method == "POST":
        user_name = request.form["username"]
        user_email = request.form["email"]
        user_password = request.form["password"]
        return redirect("/successful_registration")
    else:
        return render_template("email_verification")


@app.route(str(url.successful_registration))
def successful_registration():
        global reg
        reg = True
        return render_template("successful_registration.html")


@app.route(str(url.games))
def games():
    return render_template("games.html")
