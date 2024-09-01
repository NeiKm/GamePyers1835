"""
Этот файл отвечает за определение моделей базы данных для веб-приложения.

Модели в Flask-SQLAlchemy представляют собой классы, которые описывают структуру таблиц в базе данных. 
Каждая модель соответствует одной таблице, а атрибуты класса — это столбцы таблицы.

Что писать в этом файле:
- Определение классов моделей, которые будут использоваться для взаимодействия с базой данных.
- Настройка отношений между моделями (например, "один ко многим", "многие ко многим").
- Определение методов для работы с данными, которые могут быть специфичны для каждой модели (например, валидация данных перед сохранением).

Пример:
Класс `User` в данном файле определяет структуру таблицы для хранения информации о пользователях, где есть такие поля, как `id`, `username` и `email`. 
`id` используется как первичный ключ, а `username` и `email` должны быть уникальными и не могут быть пустыми.
"""

# from app import db  # Импортируется объект db из приложения для работы с базой данных

# Класс User определяет модель пользователя
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)  # Первичный ключ
#     username = db.Column(db.String(80), unique=True, nullable=False)  # Уникальное имя пользователя, не может быть пустым
#     email = db.Column(db.String(120), unique=True, nullable=False)  # Уникальный email, не может быть пустым