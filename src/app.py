import multiprocessing

from gunicorn.app.base import BaseApplication
from flask import Flask
from flask_cors import CORS

import app_pre_process

import os
import sys
import json

class StandaloneApplication(BaseApplication):

    options = {
        'bind': '%s:%s' % ('0.0.0.0', os.getenv("PROXY_PORT", '8080')),
        'workers': 1,
        'threads': 1,
        'timeout': 30,
        'debug': True,
        'backlog': 2048,
        'env': "dev",
        # "_ext_option":{}
    }

    def __init__(self, application_class, module, config):
        self.options = {**self.options, **{key.lower(): value for key, value in config.items() if key.lower() in self.options}}
        print(self.options)
        config.pop("BIND")
        app = application_class(module, config)
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        # for key, value in self.options.items():
        #     if key != "_ext_option":
        #         upperKey = key.upper()
        #         if upperKey in config:
        #             config[upperKey] = value
        #     else:
        #         config[key] = value
        return self.application


if __name__ == '__main__':
    path = os.path.dirname(sys.argv[0])
    with open(path+"/default-config.json","r") as f:
        config = json.load(f)
        StandaloneApplication(app_pre_process.MyApp, __name__, config).run()
