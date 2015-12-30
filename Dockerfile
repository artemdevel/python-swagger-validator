FROM python:slim

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN set -x && \
    pip install -r requirements.txt

EXPOSE 8000
CMD ["./run_app.py"]
