import os
import sys
import json
import logging
import jupyter_client

from flask import Flask, request, jsonify, abort, g
from flask_cors import CORS
from jupyter_client.manager import start_new_kernel
from IPython.utils.capture import capture_output

logging.getLogger().setLevel(logging.DEBUG)
console_logger = logging.getLogger("__debug__")
km, kc = jupyter_client.manager.start_new_kernel(kernel_name='python3')

class MyFlask(Flask):
    def __init__(self, module, config):
        Flask.__init__(self, module)
        # print(self.config)
        self.config = {**self.config, **config}
        # print(self.config)
        self.route("/", methods=["POST"])(self.execute)

    def execute(self):
        print("execute")
        try:
            with capture_output() as io:
                reply = kc.execute_interactive(request.get_data().decode(), timeout=30)
                err = io.stderr
                result = io.stdout
                return (result,200) if reply["metadata"]["status"]== "ok" else (err,500)
        except Exception as e:
            console_logger.error(str(e))
            return str(e), 500, {"Content-Type": "application/json; charset=utf-8"}

    def run(self, host=None, port:int=None, **options):
        _bind = self.config.get("BIND")
        _host, _, _port = (None, None, None) if _bind == None else _bind.partition(":")
        return Flask.run(self, host or _host, port or _port, **options)

if __name__ == '__main__':
    path = os.path.dirname(sys.argv[0])
    with open(path+"/default-config.json","r") as f:
        config = json.load(f)
        app = MyFlask(__name__, config)
        CORS(app)
        app.run()