import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create(self, table_name, columns):
        """
        Создание новой таблицы.
        Аргументы:
        - table_name (str): название таблицы.
        - columns (dict): словарь с названиями колонок и их типами данных.
        Пример: {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"}
        """
        columns_with_types = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        sql_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"
        self.cursor.execute(sql_query)
        self.connection.commit()
        print(f"Таблица: '{table_name}' успешно создана.")

    def check_and_insert (self, user_name, password, email, create = True):
        responce = self.fetch(table_name="user")
        for i in responce:
            #i[2] = ники, i[4] = пароли, i[1] = email
            if user_name in i[2] and email in i[1]:
                print(f"Пользователь {user_name} уже существует")
                if create:
                    return False
                if not create:
                    return True
        if create:
            self.insert(table_name="user", data={"user_name": str(user_name),
                                                 "name": str(user_name),
                                                 "email": str(email),
                                                 "password": str(password)
                                                })
            print(f"Пользователь {user_name} создан")
            return True

    def insert(self, table_name, data):
        """
        Вставка данных в таблицу.
        Аргументы:
        - table_name (str): название таблицы.
        - data (dict): данные для вставки (в виде словаря).
        Пример: {"name": "John", "age": 30}
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = tuple(data.values())
        sql_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql_query, values)
        self.connection.commit()
        print(f"Данные успешно добавлены в таблицу '{table_name}'.")
        return True

    def update(self, table_name, updates, condition):
        """
        Обновление данных в таблице.
        Аргументы:
        - table_name (str): название таблицы.
        - updates (dict): данные для обновления.
        - condition (str): условие для обновления (например, "id = 1").
        Пример: {"age": 35}, "name = 'John'"
        """
        updates_string = ", ".join([f"{col} = ?" for col in updates])
        values = tuple(updates.values())
        sql_query = f"UPDATE {table_name} SET {updates_string} WHERE {condition}"
        self.cursor.execute(sql_query, values)
        self.connection.commit()
        print(f"Данные в таблице '{table_name}' обновлены.")

    def delete(self, table_name, condition):
        """
        Удаление данных из таблицы.
        Аргументы:
        - table_name (str): название таблицы.
        - condition (str): условие для удаления данных (например, "id = 1").
        """
        sql_query = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(sql_query)
        self.connection.commit()
        print(f"Данные из таблицы '{table_name}' удалены.")

    def fetch(self, table_name, columns="*", condition=None):
        """
        Получение данных из таблицы.
        Аргументы:
        - table_name (str): название таблицы.
        - columns (str или list): колонки для выборки. По умолчанию "*".
        - condition (str): условие для выборки данных (например, "age > 30"). Опционально.
        """
        if isinstance(columns, list):
            columns = ", ".join(columns)
        sql_query = f"SELECT {columns} FROM {table_name}"
        if condition:
            sql_query += f" WHERE {condition}"
        self.cursor.execute(sql_query)
        results = self.cursor.fetchall()
        return results

    def drop_table(self, table_name):
        """
        Удаление таблицы.
        Аргументы:
        - table_name (str): название таблицы.
        """
        sql_query = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(sql_query)
        self.connection.commit()
        print(f"Таблица '{table_name}' удалена.")

    def close(self):
        """Закрытие соединения с базой данных."""
        self.connection.close()
        print("Соединение с базой данных закрыто.")
