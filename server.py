from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

HOST = ''
PORT = 33000
BUFFER_SIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

clients = {}
addrs = {}

def broadcast(msg, prefix = ""):
	#send a message visible to all clients
	for sock in clients:
		sock.send(bytes(prefix,"utf8")+msg)

def accept_incoming_clients():
	#to accept incoming connections
	while True:
		client, client_addr = SERVER.accept()
		print(client_addr, " connected")
		greet_msg = 'Hello! Type your username and Lestok..'
		client.send(bytes(greet_msg, "utf8"))
		addrs[client] = client_addr
		Thread(target = handle_client, args=(client,)).start()

def handle_client(client):
	#to handle one client at a time
	name = client.recv(BUFFER_SIZE).decode("utf8")
	welcome_msg = 'Welcome {}! Type quit to exit.'.format(name)
	client.send(bytes(welcome_msg, "utf8"))
	msg = "{} joined the chat!".format(name)
	broadcast(bytes(msg,"utf8"))
	clients[client] = name

	while True:
		msg = client.recv(BUFFER_SIZE)
		if msg != bytes('quit', "utf8"):
			broadcast(msg, name + ": ")
		else:
			client.send(bytes('quiting!', "utf8"))
			client.close()
			del clients[client]
			broadcast(bytes("{} left the chat.".format(name), "utf8"))
			break


if __name__ == "__main__":
	SERVER.listen(5)
	print("Waiting for connection.......")
	ACCEPT_THREAD = Thread(target = accept_incoming_clients)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()


