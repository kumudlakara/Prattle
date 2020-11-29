import sqlite3

chatroom_serv_connection = sqlite3.connect("/home/kmd/prattle/user_info.db")
cursor = chatroom_serv_connection.cursor()

#show all available chatrooms
def all_rooms():
	room_list = []

	cursor.execute("SELECT server_room FROM chatroom_server")
	chatrooms_list = cursor.fetchall()
	for i in range(len(chatrooms_list)):
		room_list.append(chatrooms_list[i][0])
	return room_list

#register new chatroom
def reg_room(room_name, iden):
	sql = """INSERT INTO chatroom_server 
	(id, server_room) VALUES('{}','{}')""".format(iden, room_name)
	val = (iden, room_name)
	cursor.execute(sql)
	chatroom_serv_connection.commit()

