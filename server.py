import time
from datetime import datetime

from flask import Flask, Response, request

app = Flask(__name__)
db = [
    {'text': 'Привет', 'author': 'Jack', 'time': time.time()},
    {'text': 'Приве!', 'author': 'Mary', 'time': time.time()},
]


@app.route("/")
def hello():
    return "Hello, World!<br><a href='/status'>Статус</a>"


@app.route("/status")
def status():
    dn = datetime.now()
    return {
        'status': True,
        'name': 'Skillbox Messenger',
        'time': dn.strftime('%Y-%m-%d %H:%M:%S'),
    }


@app.route("/send_message", methods=['POST'])
def send_message():
    data = request.json
    if not isinstance(data, dict):
        return Response('not json', 400)

    text = data.get('text')
    author = data.get('author')

    if isinstance(text, str) and isinstance(author, str):
        db.append({
            'text': text,
            'author': author,
            'time': time.time()
        })
        return Response('ok')
    else:
        return Response('wrong format', 400)


@app.route("/get_messages")
def get_messages():
    after = request.args.get('after', '0')
    try:
        after = float(after)
    except:
        return Response('wrong format', 400)

    new_messages = [m for m in db if m['time'] > after]
    return {'messages': new_messages}


app.run()
