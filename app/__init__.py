"""
Этот файл является инициализирующим модулем для приложения Flask.

Назначение файла __init__.py:
- Создает экземпляр приложения Flask.
- Настраивает и инициализирует основные компоненты приложения, такие как база данных, расширения и конфигурации.
- Определяет и регистрирует основные маршруты и обработчики ошибок.
- Файл также используется для импортирования и настройки различных частей приложения (например, моделей, форм, маршрутов).

Что писать в этом файле:
- Создание и конфигурация объекта Flask.
- Подключение базы данных через SQLAlchemy.
- Подключение и настройка расширений Flask (например, Flask-Migrate, Flask-Login).
- Импорт и регистрация синих принтов (blueprints) для организации маршрутов и их логики.
- Импорт и инициализация других компонентов, необходимых для работы всего приложения.

Пример:
В этом файле создается приложение Flask, инициализируется база данных и подключаются все необходимые компоненты.
"""

# from flask import Flask  # Импортируется класс Flask для создания приложения
# from flask_sqlalchemy import SQLAlchemy  # Импортируется SQLAlchemy для работы с базой данных
# from config import Config  # Импортируется класс Config для конфигурации приложения

# app = Flask(__name__)  # Создание экземпляра Flask
# app.config.from_object(Config)  # Загрузка конфигурации из класса Config

# db = SQLAlchemy(app)  # Инициализация базы данных с помощью SQLAlchemy

# from app import routes, models  # Импорт маршрутов и моделей для регистрации в приложении

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'kirill.kim.0223@gmail.com'
app.config['MAIL_PASSWORD'] = 'xhfr xkuk lpvg nlps'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

from app import routes
