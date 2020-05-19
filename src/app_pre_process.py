from flask import Flask, request, jsonify, abort, g
import json
import logging

import jupyter_client
from jupyter_client.manager import start_new_kernel
from IPython.utils.capture import capture_output

logging.getLogger().setLevel(logging.DEBUG)
console_logger = logging.getLogger("__debug__")
km, kc = jupyter_client.manager.start_new_kernel(kernel_name='python3')

import time

time.gmtime


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
    config = {
        "BIND": "127.0.0.1:8888",
        "ENV": "dev",
        "DEBUG": True,
    }
    app = MyFlask(__name__, config)
    # app.config["SERVER_NAME"] = config["BIND"]
    # print(app.config)
    app.run()