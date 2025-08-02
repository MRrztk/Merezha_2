from flask import Flask, request
from flask_socketio import SocketIO, send, disconnect
import os, random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

# Зберігаємо імена користувачів за session ID
users = {}

@app.route('/')
def index():
    return 'Сервер працює!'

@socketio.on('sergunchik')
def lox():
    send('Меня зовут Кира Йошикагэ. Мне 33 года. Мой дом находится в северо-восточной части Морио, в районе поместий. Работаю в офисе сети магазинов Kame Yu и домой возвращаюсь, самое позднее, в восемь вечера. Не курю, выпиваю изредка. Ложусь спать в 11 вечера и убеждаюсь, что получаю ровно восемь часов сна, несмотря ни на что. Перед сном я пью тёплое молоко, а также минут двадцать уделяю разминке, поэтому до утра сплю без особых проблем. Утром я просыпаюсь, не чувствуя ни усталости, ни стресса, словно младенец. На медосмотре мне сказали, что никаких проблем нет. Я пытаюсь донести, что я обычный человек, который хочет жить спокойной жизнью. Я не забиваю себе голову проблемами вроде побед или поражений, и не обзавожусь врагами, из-за которых не мог бы уснуть. Я знаю наверняка: в таком способе взаимодействия с обществом и кроется счастье. Хотя, если бы мне пришлось сражаться, я бы никому не проиграл.')

@socketio.on('connect')
def handle_connect():
    print(f"[ПІДКЛЮЧЕННЯ] Клієнт: {request.sid}")

@socketio.on('set_username')
def handle_set_username(username):
    users[request.sid] = username
    print(f"[ІМʼЯ ВСТАНОВЛЕНО] {request.sid} тепер '{username}'")
    send(f"{username} приєднався до чату.", broadcast=True)

@socketio.on('message')
def handle_message(msg):
    username = users.get(request.sid, "Анонім")
    full_msg = f"{username}: {msg}"
    print(f"[ПОВІДОМЛЕННЯ] {full_msg}")
    send(full_msg, broadcast=True)

@socketio.on('random')
def generate_number():
    resultNum = random.randint(0,100)
    send(resultNum, broadcast=True)

@socketio.on('reserved')
def reserved():
    send(f"Ваша кастомна функція =>", to=request.sid)


@socketio.on('users')
def list_users(data=None):
    if data is None:
        data = ''
    
    user_list = list(users.values())
    send(f"[SERVER] Active users: {', '.join(user_list)}", to=request.sid)
    
    if data == 'start':
        print('emit success DMs')
        socketio.emit("private_message", {'clients': users}, to=request.sid)


        
@socketio.on('send_dm')   
def send_dm_msg(data):
    send(f"Receiver: {data['rcver']}, message: {data['msg']}", to=data['rcver'])

@socketio.on('disconnect')
def handle_disconnect():
    username = users.pop(request.sid, "Анонім")
    print(f"[ВІДКЛЮЧЕННЯ] {username} ({request.sid})")
    send(f"{username} вийшов з чату.", broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
