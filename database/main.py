import sqlite3
from DATABASE import DatabaseManager

# "id": "INTEGER PRIMARY KEY",
# "user_name": "TEXT",
# "name": "TEXT",
# "password": "TEXT"


if __name__ == "__main__":
    db = DatabaseManager("database/USER.db")
    # db.create(table_name="user", columns={
    #                                       "id": "INTEGER PRIMARY KEY",
    #                                       "email": "TEXT",
    #                                       "user_name": "TEXT",
    #                                       "name": "TEXT",
    #                                       "password": "TEXT"
    #                                       })
    # db.insert(table_name="user", data={"user_name": "Nei_km",
    #                                    "name": "kirill",
    #                                    "email": "kirill.kim.0223@gmail.com",
    #                                    "password": "kirillkim2009232"
    #                                    })
    # db.delete(table_name="user", condition="id=2")
    # print(db.check_and_insert(user_name="Nei_km2", password="kirillkim2009232", email="kirill.kim.0223@gmail.com"))
    
    res = db.fetch(table_name="user")
    for i in res:
        print(i)
    db.close()
