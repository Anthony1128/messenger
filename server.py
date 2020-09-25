import time
from datetime import datetime
from flask import Flask, request, abort


app = Flask(__name__)
db = []


# стартовая страница мессенджера со ссылкой на страницу статуса
@app.route('/')
def start_page():
    return 'Welcome, see <a href="/status">status</a> for information'


# страница статуса мессенджера
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


# функция отправки сообщений
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


# список сообщений
@app.route('/messages')
def messages():
    if 'after_timestamp' in request.args:
        after_timestamp = float(request.args['after_timestamp'])
    else:
        after_timestamp = 0

    # пагинация
    max_limit = 100
    if 'limit' in request.args:
        limit = int(request.args['limit'])
        if limit > max_limit:
            abort(400, 'too big limit')
    else:
        limit = max_limit

    # подсчет сообщений которые надо вернуть
    after_id = 0
    for message in db:
        if message['timestamp'] > after_timestamp:
            break
        after_id += 1

    return {'messages': db[after_id:after_id+limit]}


# запуск сервера
app.run()




