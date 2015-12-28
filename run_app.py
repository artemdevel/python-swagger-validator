#!/usr/bin/env python
from app import create_app
from werkzeug.serving import run_simple


if __name__ == '__main__':
    app = create_app()
    run_simple('127.0.0.1', 8000, app, use_reloader=True)
