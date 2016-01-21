#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
set -x


BUILD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
cd "$BUILD_DIR"

docker build -t python_swagger_validator .
docker run --name swagger-validator -e APP_ADDR=0.0.0.0 -dp 127.0.0.1:7777:8000 python_swagger_validator
