from PyQt5 import QtWidgets, QtCore
from clientui import Ui_MainWindow
from datetime import datetime
import requests


# messenger with interface from client.ui
class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)

        self.url = url
        self.after_timestamp = 0
        self.pushButton.pressed.connect(self.button_pressed)

        # load all messages from database
        self.load_messages

        # load new messages every second
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    # message input in readable form
    def pretty_print(self, message):
        dt = datetime.fromtimestamp(message['timestamp'])
        dt = dt.strftime('%Y/%m/%d %H:%M:%S')
        first_line = dt + ' ' + message['name']
        self.textBrowser.append(first_line)
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')
        self.textBrowser.repaint()

    # message upload
    def update_messages(self):
        response = None
        messages = None
        try:
            response = requests.get(self.url + '/messages',
                                    params={'after_timestamp': self.after_timestamp})
        except:
            pass

        # check connection, new messages
        # and fixing last loaded message
        if response and response.status_code == 200:
            messages = response.json()['messages']
            for message in messages:
                self.pretty_print(message)
                self.after_timestamp = message['timestamp']
        return messages

    # load all old messages
    def load_messages(self):
        while self.update_messages():
            pass

    # function for sending message button
    def button_pressed(self):
        name = self.lineEdit.text()
        text = self.textEdit.toPlainText()
        data = {'name': name, 'text': text}
        response = None
        try:
            response = requests.post(self.url + '/send', json=data)
        except:
            pass

        # test connection with server
        if response and response.status_code == 200:
            self.textEdit.clear()
            self.textEdit.repaint()
        else:
            self.textBrowser.append('Server error')
            self.textBrowser.repaint()


# app entrypoint
app = QtWidgets.QApplication([])
ip_address = 'http://127.0.0.1:5000/' # or ngrok's ip
window = Messenger('{}'.format(ip_address))
window.show()
app.exec_()




