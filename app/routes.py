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


from flask import render_template, request, redirect, make_response
from flask_mail import Mail, Message
from app.config import URL
import random
from app import app
from database.DATABASE import DatabaseManager


def send_email(user_email, text):
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


mail = Mail(app)
url = URL()
user_db = DatabaseManager("database/USER.db")
posts_db = DatabaseManager("database/POSTS.db")


@app.route("/home")
@app.route("/")
def index():
    print(request.cookies.get("join_date"))
    response = make_response()
    logged = request.cookies.get("logged")
    print(logged)
    
    if logged == "yes":
        reg_or_profil = "Профиль"
        url_reg_or_profil = url.profil
    else:
        reg_or_profil = "Зарегистрироваться"
        response.delete_cookie("user_name")
        url_reg_or_profil = url.create_account

    user_name = request.cookies.get("user_name")

    response.set_data(render_template(
        "index.html",
        user_name=user_name if user_name else "Гость",
        reg_or_profil=reg_or_profil,
        url_reg_or_profil=url_reg_or_profil
    ))

    return response


@app.route(str(url.news))
def news():
    # Сделать бд для новостей и сделать страничку управление 222
    return render_template("news.html")


@app.route(str(url.profil))
def profil():
    return render_template(
        "profil.html",
        user_name = request.cookies.get("user_name"),
        email = request.cookies.get("email"),
        joined = request.cookies.get("join_date")
    )


@app.route("/delete_post", methods=["POST"])
def delete_post():
    post_id = request.form.get("post_id")

    posts_db.delete(table_name="posts", condition=f"id = {post_id}")
    
    return redirect("/posts")


@app.route("/launcher")
def launcher():
    # Доделать функционал и внешний вид 111
    return render_template("launcher.html")


@app.route("/edit_post", methods=["POST"])
def edit_post():
    post_id = request.form.get("post_id")
    
    post = posts_db.fetch(table_name="posts", condition=f"id = {post_id}")
    
    if post:
        return render_template("edit_post.html", post=post[0])
    else:
        return "Пост не найден"


@app.route(str(url.posts), methods=["POST", "GET"])
def posts():
    try:
        user_name = request.cookies.get("user_name")
    except:
        user_name = "Гость"

    this_user = user_db.fetch(
        table_name="user", 
        condition=f"user_name = '{user_name}'"
    )

    if not this_user:
        response = response = make_response(render_template(
        "message.html", 
        title = f"Для этой функции необходим аккаунт",
        text = f"""
                Чтобы пользоваться функцией создания и редактирования постов, а также просматривать их,
                вам необходимо войти в свой аккаунт или создать новый.
                """
        ))
        return response

    user_id = this_user[0][0]

    if request.method == "POST":

        posts_db.insert(
            table_name="posts",
            data={
                "user_id": str(user_id),
                "content": str(request.form["post_content"])
            }
        )

    user_posts = posts_db.fetch(
        table_name="posts",
        condition=f"user_id = {user_id}"
    )

    return render_template("posts.html", my_post=user_posts)


@app.route(str(url.logout))
def out():
    res = make_response(redirect("/"))
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

        users = user_db.fetch(
            table_name="user", 
            condition=f"user_name = '{user['name']}' AND password = '{user['password']}' AND email = '{user['email']}'"
        )

        if users:
            print("Пользователь существует")
            response = make_response(redirect(str(url.email_verification)))
            response.set_cookie("logged", "yes")
            response.set_cookie("user_name", user["name"])
            response.set_cookie("email", user["email"])
            response.set_cookie("join_date", str(users[0][5]))

            return response
        
        response = make_response(
            render_template(
                "message.html", 
                title="Ошибка",
                text="Неверное имя пользователя или пароль."
            )
        )

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
        
            existing_user = user_db.fetch(
                table_name="user", 
                condition=f"user_name = '{user['name']}' OR email = '{user['email']}'"
            )

            print(existing_user)

            if existing_user:
                return make_response(
                    render_template(
                        "message.html", 
                        title="Ошибка регистрации",
                        text="Пользователь с таким именем или email уже существует. Пожалуйста, используйте другие данные."
                    )
                )

            if user["password"] == user["confirm_password"]:
                db_answer = user_db.insert(
                    table_name="user",
                    data={"user_name": user["name"], "email": user["email"], "password": user["password"]}
                )
                if db_answer:
                    response = make_response(redirect(str(url.email_verification)))
                    response.set_cookie("user_name", user['name'])
                    response.set_cookie("email", user["email"])
                    response.set_cookie("password", user["password"])
                else:
                    response = make_response(render_template(
                        "message.html", 
                        title="Ошибка регистрации",
                        text="Произошла ошибка при создании аккаунта. Попробуйте снова."
                    ))
        else:
            response = make_response(render_template(
                "message.html", 
                title="Ошибка регистрации",
                text="Введённые пароли не совпадают. Пожалуйста, проверьте правильность ввода и попробуйте снова."
            ))

    return response


@app.route(str(url.email_verification), methods=["POST", "GET"])
def email_verification():
    if request.cookies.get("email_verification_sent") != "yes":
        if request.cookies.get("verification_code") is None:
            really_verification_code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            send_email(request.cookies.get("email"), really_verification_code)
            response = make_response(render_template("email_verification.html"))
            response.set_cookie("email_verification_sent", "yes", max_age=15)
            response.set_cookie("verification_code", str(really_verification_code))
            return response


    if request.method == "POST":
        verification_code = request.form.get("verification_code")
        print(f"________________________________| {verification_code} |________________________________")
        stored_verification_code = request.cookies.get("verification_code")

        if verification_code != stored_verification_code:
            response = response = make_response(render_template(
                "message.html", 
                title = f"Неверный код подтверждения email.",
                text = f"""
                        Неверный код подтверждения email. Пожалуйста, проверьте код и повторите попытку."""
                ))
            return response
        else:
            try:
                db_answer = user_db.check_and_insert(user_name=request.cookies.get("user_name"), 
                                                     password=request.cookies.get("password"),
                                                     email=request.cookies.get("email"))
                if db_answer:
                    response = make_response(redirect(str(url.email_verification)))
                    response.set_cookie("logged", "yes")
                else:
                    response = response = make_response(render_template(
                        "message.html", 
                        title = f"Пользователь {str(request.cookies.get('user_name'))} уже существует",
                        text = f"""
                                Пользователь с такими данными (имя, пароль, email) уже существует в нашей системе. 
                                Пожалуйста, используйте другие данные для регистрации или войдите в систему с текущими данными."""
                        ))
            except Exception as e:
                print(f"Ошибка базы данных: {e}")
                response = make_response(f"Ошибка базы данных: {e}")

            response = redirect(str(url.successful_registration))
            response.set_cookie("logged", "yes")
            return response

    return render_template("email_verification.html")


@app.route(str(url.successful_registration))
def successful_registration():
    return render_template("successful_registration.html")


@app.route(str(url.games))
def games():
    return render_template("games.html")
