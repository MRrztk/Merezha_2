import socketio

RENDER_SERVER_URL = 'https://merezha-2-vd0s.onrender.com'
USERNAME = input("Придумай собі прізвисько =)\n ")

sio = socketio.Client()

@sio.event
def connect():
    print("[✔️] Підключений до серверу.")
    sio.emit("set_username", USERNAME)

@sio.on('message')
def on_message(data):
    print(data)

@sio.on("private_message")
def send_message_private(data):
    print("[CLIENT] Received private message user list.")
    global private_message_clients
    private_message_clients = data['clients']


@sio.event
def disconnect():
    print("[❌] Кікнуто.")

try:
    print(f"[...] Йдемо в гості до {RENDER_SERVER_URL} ...")
    sio.connect(RENDER_SERVER_URL)
except Exception as e:
    print("[‼️] Трабли зі з'єднанням:", e)
    exit()

private_message_clients = None  # global variable to track state

try:
    while True:
        msg = input()

        if msg.lower() == "exit":
            break
        elif msg.lower() == 'randomito':
            sio.emit("random")
            continue
        elif msg.lower() == '/users':
            sio.emit("users")
            continue
        elif msg.lower() == '/private':
            sio.emit("users", 'start')
            continue

        elif msg.lower() == "":
            sio.emit('sergunchik')
            continue


        # Handle private message after receiving client list
        if private_message_clients:
            print("=== Direct Message Mode ===")
            receiver = input('Введіть прізвисько отримувача:\n')
            forwarded_msg = input('Лист отримувачу пишіть тут:\n')
            user_sid = None
            for sid, name in private_message_clients.items():
                if name == receiver:
                    user_sid = sid
                    break
            if user_sid:
                rcv_info = {"msg": forwarded_msg, 'rcver': user_sid}
                sio.emit("send_dm", rcv_info)
            else:
                print("User not found.")
            private_message_clients = None  # reset the flag
            continue

        # Otherwise send normal message
        sio.send(msg)

except KeyboardInterrupt:
    pass
finally:
    sio.disconnect()
