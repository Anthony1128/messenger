import time
from datetime import datetime
from flask import Flask, request, abort


app = Flask(__name__)
db = []


# messenger starting page with link to status page
@app.route('/')
def start_page():
    return 'Welcome, see <a href="/status">status</a> for information'


# messenger status page
@app.route('/status')
def status():
    date_now = datetime.now()
    date_data = {
        'status': True,
        'name': 'Messenger',
        'time': date_now.strftime('%d.%m.%Y %H:%M:%S'),
        'users': len(set(message['name'] for message in db))
    }
    return date_data


# send message function
@app.route('/send', methods=['POST'])
def send():
    data = request.json
    db.append({
        'id': len(db),
        'name': data['name'],
        'text': data['text'],
        'timestamp': time.time()
    })
    return {'ok': True}


# list of messages
@app.route('/messages')
def messages():
    if 'after_timestamp' in request.args:
        after_timestamp = float(request.args['after_timestamp'])
    else:
        after_timestamp = 0

    # pagination
    max_limit = 100
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        if limit > max_limit:
            abort(400, 'too big limit')
    else:
        limit = max_limit

    # count messages that should be returned
    after_id = 0
    for message in db:
        if message['timestamp'] > after_timestamp:
            break
        after_id += 1

    return {'messages': db[after_id:after_id+limit]}


# server entrypoint
app.run()




