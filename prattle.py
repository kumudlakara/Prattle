import os
import sys
import time
import user_login_auth
import chatroom_server
from pusher import Pusher
import pysher
import json
from termcolor import colored,cprint
from PyInquirer import style_from_dict, Token, prompt
from dotenv import load_dotenv
from progress.bar import FillingCirclesBar
from os import path
import random


load_dotenv(dotenv_path='prattle.env')

class Prattle:
	
	pusher = None
	channel = None
	clientPusher = None
	user = None
	users = dict()

	chatrooms = []
	chatrooms = chatroom_server.all_rooms()

	temp_data = user_login_auth.find_user()
	for i in temp_data:
		users[i[0]] = i[1]

	#create diff folder for download and upload
	temp_dir = os.getcwd()
	os.chdir("/home/kmd/prattle/")
	if path.isdir("prattle_downloads") == True:
		pass
	else:
		os.system('mkdir prattle_downloads')

	if path.isdir("prattle_to_upload") == True:
		pass
	else:
		os.system('mkdir prattle_to_upload')

	os.chdir(temp_dir)
	#animation
	def sleep(self):
		t = 0.02
		t += t*random.uniform(-0.1,0.1)
		time.sleep(t)
	def welcome(self):
		cprint(" Greetings from Prattle!", 'green', attrs=['bold'], file=sys.stderr)
		time.sleep(1)
		cprint("Lets Prattle!", 'green', attrs=['bold'], file=sys.stderr)

    #login and register new users
	def logincred(self):
		style = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#00FFFF',
        Token.Instruction: '', 
        Token.Answer: '#2196f3 bold',
        Token.Question: '#7FFF00 bold',
        })
        #Using PyInquirer for Dropdown menu interface
		time.sleep(0.2)
		questions=[ 
            {
                'type':'list',
                'name':'log',
                'message':'Choose one :',
                'choices': ['login','registration'],
                'default':'login'
            }
        ]

		answers=prompt(questions,style=style)
        
        #Loading bar animation
		os.system('clear')
		time.sleep(0.05)
		print("")
		#########################################################
		suffix = '%(index)d/%(max)d [%(elapsed)d / %(eta)d / %(eta_td)s]'
		bar = FillingCirclesBar(" loading ", suffix=suffix)
		for i in bar.iter(range(100)):
		    self.sleep()
		#########################################################
		time.sleep(1.0)
		os.system("clear")
		cprint("Connected...", "green", attrs =['bold'])
		time.sleep(0.5)
		os.system('clear')

		#get user data from database
		user1 = dict()
	
		temp_data = user_login_auth.find_user()
		for i in temp_data:
			user1[i[0]] = i[1]
		self.users = user1

		if answers['log'] == 'login':
			username = input(" username: ")
        	#use getpaass to hide password
			password = getpass.getpass(" password: ")
			time.sleep(0.1)
			print("")

        	#check if user is in database
			if username in self.users:
        		#check password
				if self.users[username] == password:
					self.user = username
					cprint(" logged in successfullly", "cyan", attrs=['bold'])
					time.sleep(1)
				else:
					cprint("Incorrect password", "red")
					print("")
					time.sleep(0.5)
					os.system('clear')
					self.logincred()
			else:
				cprint("Incorrect username!", "red")
				print("")
				time.sleep(0.5)
				os.system('clear')
				self.logincred()

		elif answers["log"] == "registration":
			
			user_login_auth.register()
			cprint("Registered Successfully!", "yellow", attrs=['bold'])
			time.sleep(1)
			self.logincred()

	 #select chatroom
	def select_chatroom(self):
		chatroom = input("Enter name of Chatroom: ")
		#add new chatroom to database
		if chatroom in self.chatrooms:
			print("")
		else:
			time.sleep(1)
			chatroom_server.reg_room(chatroom, random.randint(0,100) + random.randint(100,200) + random.randint(200,300))
			print("")
			os.system('clear')

		#get chatroom from database
		chatrooms = chatroom_server.all_rooms()
		self.chatrooms = chatrooms

		if chatroom in self.chatrooms:
			self.chatroom = chatroom
			self.initPusher()

		else:
			cprint(" No secure Chat Room found! ")
			print("")
			self.select_chatroom()

	#initialize both server Pusher as well as client Pusher
	def initPusher(self):
		self.pusher = Pusher(app_id="PUSHER_APP_ID", key="PUSHER_KEY", secret="PUSHER_SECRET", cluster="PUSHER_CLUSTER")
		self.clientPusher = pysher.Pusher("PUSHER_KEY","PUSHER_CLUSTER")
		self.clientPusher.connection.bind('pusher:connection_established', self.connectHandler)
		self.clientPusher.connect()

	#call once connection established
	def connectHandler(self, data):
		self.channel = self.clientPusher.subscribe(self.chatroom)
		self.channel.bind('newmessage', self.pusherCallback)

	#call when pusher receives a new event
	def pusherCallback(self, message):
		messsage = json.loads(message)
		if message['user'] != self.user:
			print(colored("{}: {}".format(message['user'], message['message']), "blue"))
			print(colored("{}: ".format(self.user), "green"))

    #get current message of the user
	def getInput(self):
    	#to initate file transfer in-app
		formate="["+self.user+"]: "
		message = input(colored(formate,"green"))
		if message=="send file" or message=="sdf":
            
            #importing ftpserver.py for connecting to cloud ftp server 
			import ftpserver
            
			os.chdir('/home/kmd/prattle/prattle_to_upload')
			print("")
			flt=ftpserver.uploadfile()
			message=formate+"file is uploaded.[filename = {}]".format(flt)
			print(message)
			os.chdir(self.temp_dir)

		if message == 'download file' or message == 'ddf':
			os.chdir('/home/kmd/prattle/prattle_downloads')
			import ftpserver

			ftpserver.download_file()
			os.chdir(self.temp_dir)
			message = "........"
			print(message)
			print("File downloaded")

		if message == 'exit':
			cprint("Thanks for Prattling!", "cyan", attrs=['bold'])
			time.sleep(1)
			os.system('clear')
			self.main()

		if message == "open file":
			os.chdir('/home/kmd/prattle/prattle_downloads')
			fl=input(" [system]: filename -> ")
			filename = '/home/kmd/prattle/prattle_downloads/'+str(fl)
			os.open(filename,os.O_RDWR )
			#os.chdir(self.temp_dir)
			os.close()
			message="......."
			print(message)   
		self.pusher.trigger(self.chatroom, u'newmessage', {"user": self.user, "message": message})


	def main(self):
		os.system('clear')
		self.welcome()
		self.logincred()
		self.select_chatroom()
		while True:
			self.getInput()


if __name__ == "__main__":
	Prattle().main()




