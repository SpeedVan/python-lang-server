from flask import Flask, request, render_template
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.exceptions import WebSocketErrorimport json

app = Flask(__name__)

user_socket_list = []

@app.route('/')
def index():
    return render_template('ws.html')


@app.route('/chat')
def chat():
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    user_socket_list.append(user_socket)
    print(len(user_socket_list), user_socket_list)
    try:
        while True:
            msg = user_socket.receive()
            for socket in user_socket_list:
                if socket != user_socket_list:
                    socket.send(json.dumps({"msg": msg})) # " 服务器信息: " +
    except WebSocketError as e:
        print(e)
        user_socket_list.remove(user_socket)
        return ''


if __name__ == '__main__':
    http_server = WSGIServer(('192.168.56.1', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()