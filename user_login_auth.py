import sqlite3

connection = sqlite3.connect("/home/kmd/prattle/user_info.db")
cursor = connection.cursor()

#register new user
def register(user_id, name, username, password):
	sql = "insert into user (user_id, name, username, password) values (%s, %s, %s, %s);"
	val = (user_id,name, username, password)
	try:
		cursor.execute(sql,val)
		#cursor.execute("INSERT INTO user (user_id, name, username, password) VALUES (%s, %s, %s, %s);",val)
		connection.commit()
		return 0
	except:
		return 1

#user login
def login(username, password):
	sql = "SELECT username, password FROM user_info.user;"
	cursor.execute(sql)
	result = cursor.fetchall()
	check = 0
	for user in result:
		if user[0] == username and user[1] == password:
			check = 1;

	if check == 1:
		return 0
	else:
		return 1

#find user in database
def find_user():
	cursor.execute("SELECT username, password FROM user;")
	user_details = cursor.fetchall()
	return user_details


