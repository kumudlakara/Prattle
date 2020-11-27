import sqlite3
connection = sqlite3.connect("user_info.db")

cursor = connection.cursor()
sql_command = "CREATE TABLE user (user_id INTEGER PRIMARY KEY, name VARCHAR(50), username VARCHAR(20), password VARCHAR(30));"
#sql_command = "CREATE TABLE chatroom_server (id INTEGER PRIMARY KEY, server_room VARCHAR(50));"

cursor.execute(sql_command)

connection.commit()
connection.close()