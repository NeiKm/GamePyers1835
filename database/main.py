import sqlite3
from DATABASE import DatabaseManager

# "id": "INTEGER PRIMARY KEY",
# "user_name": "TEXT",
# "name": "TEXT",
# "password": "TEXT"

# db.create(table_name="posts", columns={
#                                       "id": "INTEGER PRIMARY KEY",
#                                       "user_id": "INTEGER",
#                                       "content": "TEXT",
#                                       "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
#                                       })

if __name__ == "__main__":
    db = DatabaseManager("database/USER.db")
    posts_db = DatabaseManager("database/POSTS.db")
    # db.create(table_name="user", columns={
    #                                       "id": "INTEGER PRIMARY KEY",
    #                                       "email": "TEXT",
    #                                       "user_name": "TEXT",
    #                                       "name": "TEXT",
    #                                       "password": "TEXT",
    #                                       "join_date": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    #                                       })
    # db.insert(table_name="user", data={"user_name": "Nei_km",
    #                                    "name": "kirill",
    #                                    "email": "kirill.kim.0223@gmail.com",
    #                                    "password": "123"
    #                                    })

    # posts_db.delete(
    #     table_name="posts",
    #     condition="id=4"
    # )

    # db.delete(table_name="user", condition="id=1")
    # print(db.check_and_insert(user_name="Nei_km2", password="kirillkim2009232", email="kirill.kim.0223@gmail.com"))
    
    # res1 = posts_db.fetch(table_name="posts")
    # for i in res1:
    #     print(i)

    res2 = db.fetch(table_name="user")
    for i in res2:
        print(i)

    # users = db.fetch(table_name="user", condition="email = 'nei.km.0223@gmail.com'")
    # print(users)
    #for u in users:
    #    if "Nei_km" in u and "kirillkim2009232" in u and "kirill.kim.0223@gmail.com" in u:
    #        print(u)

    db.close()
