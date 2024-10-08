"""

Этот файл используется для запуска приложения Flask.

Назначение файла run.py:
- Основная точка входа для запуска приложения.
- Здесь определяется, как и где будет запускаться приложение (например, в режиме отладки, на каком хосте и порте).
- Может быть использован для запуска приложения локально или в режиме разработки.

Что писать в этом файле:
- Импорт приложения Flask из инициализирующего модуля (`__init__.py`).
- Определение конфигурации запуска (например, режим отладки, хост, порт).
- Запуск приложения с помощью метода `run()`.

Пример:
В этом файле запускается приложение Flask с заданными параметрами хоста и порта, обычно используется для локальной разработки.

"""


from app import app

if __name__ == '__main__':
    app.run(debug=True)
