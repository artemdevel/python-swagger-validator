#!/usr/bin/env python
from wsgiref.simple_server import make_server

from app import create_app


if __name__ == '__main__':
    make_server('127.0.0.1', 8000, create_app()).serve_forever()
