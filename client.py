from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import ttk



def receive():
	#to handle receiving messages
	while True:
		try:
			msg = client_socket.recv(BUFFERSIZE).decode("utf8")
			msg_list.insert(tkinter.END, msg)
		except OSError:
			#if client leaves the chat
			break

def send(event = None):
	#to handle sending messages
	msg = my_msg.get()
	my_msg.set("")
	client_socket.send(bytes(msg, "utf8"))
	if msg == "quit":
		client_socket.close()
		top.destroy()

def on_closing(event = None):
	my_msg.set("quit")
	send()

top = tkinter.Tk()
top.title("LesTok")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("")
scrollbar = ttk.Scrollbar(messages_frame, orient = tkinter.VERTICAL)
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
#pack all elements
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.wm_protocol("WM_DELETE_WINDOW"	, on_closing)


#sockets
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
	PORT = 33000
else:
	PORT = int(PORT)

BUFFERSIZE = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()