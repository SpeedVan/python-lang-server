# python-lang-server

base on 
https://ipython.readthedocs.io/en/latest/development/how_ipython_works.html#terminal-ipython
https://github.com/jupyter/jupyter_client/blob/master/jupyter_client/tests/test_kernelapp.py

python denpendences：
```
ipykernel
flask
gunicorn
```
## local test
```
python src/app_pre_process.py
```
a flask web app will startup.

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

## Will finish
* did not get result through stdout, then "python src/app.py" would be.
* debug http interface

## design
![svg](/DESIGN.svg)
