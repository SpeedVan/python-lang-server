# python-lang-server

base on 
https://ipython.readthedocs.io/en/latest/development/how_ipython_works.html#terminal-ipython
https://github.com/jupyter/jupyter_client/blob/master/jupyter_client/tests/test_kernelapp.py

python denpendences：
```
pip install ipykernel flask flask-cors gevent gevent-websocket protobuf
```
## local test
```
python src/app_pre_process.py
```
a flask app which base on gevent wsgi will startup.

## Usage
interactive url:
```
POST /
```
body:
```
<code>
```
response:
ok:
```
200
<result>
```
fail:
```
500
<err>
```
websocket url:
```
/interactive
```

## build
pyinstaller -F src/app_pre_process.py --hidden-import google

## Will finish
* did not get result through stdout, then "python src/app.py" would be.
* debug http interface

## design
![svg](/DESIGN.svg)