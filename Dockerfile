FROM python:3.6.10



# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -yq davfs2 netcat

COPY ./pip_conf/pip_aliyun.conf /etc/pip.conf
RUN pip install --upgrade pip
RUN pip install ipykernel flask flask-cors gevent gevent-websocket protobuf
RUN mkdir /app
ADD ./src /app

WORKDIR /app

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV PYTHONUNBUFFERED 0

ENV PYTHONIOENCODING utf-8

ENTRYPOINT [ "python", "./app_pre_process.py" ]