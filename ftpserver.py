from ftplib import FTP
import os

#connect to cloud ftp server
ftp = FTP('ftp.drivehq.com')
ftp.login(user="username", passwd="**********")

#download file
def download_file():
	filename = input("filename: ")
	localfile = open(filename, "wb")
	ftp.retrbinary('RETR '+filename,localfile.write, 1024)
	ftp.quit()
	localfile.close()

#upload file
def uploadfile():
	filename = input("filename: ")
	if os.path.isfile(filename):
		ftp.storbinary('STOR '+filename, open(filename, 'rb'))
		print("file uploaded!")
		ftp.quit()
	else:
		print("ERROR ! no such file named {} exists.".format(filename))
