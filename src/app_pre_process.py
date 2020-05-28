import os
import sys
import json
import logging
import jupyter_client
import datetime
import time

from flask import Flask, request, jsonify, abort, g
from flask_cors import CORS
from jupyter_client.manager import start_new_kernel
from IPython.utils.capture import capture_output

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from geventwebsocket.exceptions import WebSocketError
from geventwebsocket.websocket import WebSocket
from proto import msg_pb2

logging.getLogger().setLevel(logging.DEBUG)
console_logger = logging.getLogger("__debug__")

class MyFlask(Flask):
    def __init__(self, module, config):
        Flask.__init__(self, module)
        # print(self.config)
        self.config = {**self.config, **config}
        # print(self.config)
        self.route("/", methods=["POST"])(self.execute)
        self.route("/interactive")(self.interactive)

        km, kc = jupyter_client.manager.start_new_kernel(kernel_name='python3')
        self.kc = kc
        self.socket_list = []

    def execute(self):
        print("execute")
        try:
            with capture_output() as io:
                reply = self.kc.execute_interactive(request.get_data().decode(), timeout=30)
                err = io.stderr
                result = io.stdout
                return (result,200) if reply["metadata"]["status"]== "ok" else (err,500)
        except Exception as e:
            console_logger.error(str(e))
            return str(e), 500, {"Content-Type": "application/json; charset=utf-8"}

    def interactive(self):
        
        km, kc = jupyter_client.manager.start_new_kernel(kernel_name='python3')
        ws = request.environ.get("wsgi.websocket")
        print("connection:", ws.environ)
        t = (ws)
        self.socket_list.append(t)
        try:
            while True:
                bs = ws.receive()
                print("check close:",ws.closed)
                if not ws.closed:
                    msg = msg_pb2.Msg()
                    msg.ParseFromString(bs)
                    print("msg", msg)
                    with capture_output() as io:
                        reply = kc.execute_interactive(bytes.decode(msg.body), timeout=30)
                        err = io.stderr
                        result = io.stdout

                    resMsg = msg_pb2.Msg()
                    resMsg.meta.traceId=msg.meta.traceId
                    if reply["metadata"]["status"]== "ok":
                        resMsg.meta.type=msg_pb2.Type.Interactive_ResOK
                        resMsg.body=str.encode(result)
                    else:
                        resMsg.meta.type=msg_pb2.Type.Interactive_ResERR
                        resMsg.body=str.encode(err)
                    print("resMsg", resMsg)
                    ws.send(resMsg.SerializeToString())
        except WebSocketError as e:
            print("WebSocketError", e)
        finally:
            ws.close()
            kc.shutdown()
            self.socket_list.remove(t)
        return ""
        
    def run(self, host=None, port:int=None, **options):
        _bind = self.config.get("BIND")
        _host, _, _port = (None, None, None) if _bind == None else _bind.partition(":")
        return super().run(host or _host, port or _port, **options)

if __name__ == "__main__":
    path = os.path.dirname(sys.argv[0])
    with open(path+"/default-config.json","r") as f:
        config:dict = json.load(f)
        print("config", config)
        bind:str = config.pop("BIND")
        addr_port = bind.split(":")
        http_server = WSGIServer((addr_port[0],int(addr_port[1])), MyFlask(__name__, config), handler_class=WebSocketHandler)
        http_server.serve_forever()
   
    