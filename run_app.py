#!/usr/bin/env python
import os
from wsgiref.simple_server import make_server

from structlog import get_logger

from app import create_app

log = get_logger()


if __name__ == '__main__':
    app_addr = os.environ.get('APP_ADDR') or '127.0.0.1'
    app_port = os.environ.get('APP_PORT') or '8000'
    log.info('Starting Swagger validator app on {}:{}'.format(app_addr, app_port))
    make_server(app_addr, int(app_port), create_app()).serve_forever()
