# Messenger
## Description
You can start local server which receives, stores messages.
It has POST method to send messages. 
By starting messenger you will have an app with graphical interface to 
send and view messages.
You can expose a local web server to the internet with ngrok.

## Get started
1. Run server `python server.py`
2. Run interface `python messenger.py`
    * _(or if you want to expose your server to the internet)_
    * Run `./ngrok http 5000` where 5000 is port from step 1.
    * Change `ip_address` in messenger.py (line 81) to new from step 2.
    * Run interface `python messenger.py`

## Tools
For this project were used:
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
for server developing
- [Qt](https://www.qt.io/) and [PyQt](https://pypi.org/project/PyQt5/)
for app interface developing
- [ngrok](https://ngrok.com/)
for exposing a local web server to the internet

    
