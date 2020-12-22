# Prattle

Prattle is a Python based terminal chat application with real-time file transfer capabilities. It makes use of sqlite3 database to store the user data and chatroom server data.

## How it works

Prattle uses Pusher to add real-time data and user functionality. The user database is used to allow user registration and log in. The chatroom database is used to add a chatroom or "world" to the application. On logging in, a user can choose to create a "new world" for the team or enter an existing world. On entering a "world" the user can upload and download files from the cloud that belongs to the team. Prattle uses DriveHQ as the cloud server for in-app file transfer using FTP. 

## Requirements

- Python 3+
- pusher 3.0.0
- DriveHQ
- PyInquirer 1.0.3
- progress 1.5
- sqlite3
- termcolor 1.1.0

## Enhancements
- Adding password protection for "worlds".
- Allowing task assignment to "world" members.



