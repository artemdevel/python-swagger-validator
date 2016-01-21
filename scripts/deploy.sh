#!/usr/bin/env bash

docker run --name swagger-validator -e APP_ADDR=0.0.0.0 -dp 127.0.0.1:7777:8000 python_swagger_validator
