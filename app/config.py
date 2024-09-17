"""
Этот файл содержит конфигурацию для веб-приложения на Flask.

В `config.py` определяются важные настройки, такие как секретный ключ для защиты данных и параметры подключения к базе данных. 
Эти параметры могут быть заданы непосредственно в коде или загружены из переменных окружения, что делает приложение более гибким и безопасным.

Что писать в этом файле:
- Определяются конфигурационные параметры, которые будут использоваться во всем приложении.
- Задаются значения переменных окружения, таких как SECRET_KEY и DATABASE_URL, для обеспечения безопасности и удобства конфигурирования.
- Создаются классы конфигураций для различных окружений (например, разработка, тестирование, продакшн).

Пример:
Если необходимо использовать SQLite базу данных в качестве хранилища, можно задать её URI прямо в коде. 
Если нужно использовать другую базу данных, можно задать её URI через переменную окружения DATABASE_URL.

"""

# import os  # Импортируется модуль os для работы с переменными окружения

# Класс Config содержит конфигурацию приложения
# class Config:
#     # Секретный ключ используется для защиты данных (например, CSRF-токенов)
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard_to_guess_string'
#     # URI базы данных: сначала пытаемся загрузить из переменной окружения, если не удается, используем SQLite
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'

class URL:
    def __init__(self) -> None:
        self.create_account = "/create_account"
        self.youtube = "https://www.youtube.com/@GamePyers"
        self.posts = "/posts"
        self.news = "/news"
        self.games = "/games"
        self.profil = "/profil"
        self.login_account = "/login_account"
        self.email_verification = "/email_verification"
        self.successful_registration = "/successful_registration"
        self.logout ="/logout"
