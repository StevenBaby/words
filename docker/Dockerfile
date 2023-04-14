# syntax = docker/dockerfile:experimental
FROM python:3.10-alpine

VOLUME /app/local
WORKDIR /app

COPY ./app /app

RUN adduser --disabled-password --gecos '' -u 1000 words 

RUN --mount=type=cache,target=~/.cache/pip \
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ \
    && chmod +x ./entrypoint.sh \
    && chown words -R .

USER words

CMD [ "/bin/sh", "./entrypoint.sh" ]

EXPOSE 8888
