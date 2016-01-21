#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
set -x

BUILD_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
cd "$BUILD_DIR"

bash -c 'type -p docker || curl -sSL https://get.docker.io/builds/Linux/x86_64/docker-1.9.1.tgz | tar zxf - -C /'

export DOCKER_HOST=tcp://studentroommatematching.com:2376
export DOCKER_TLS_VERIFY=1
export DOCKER_CERT_PATH=$BUILD_DIR/certs

docker build -t python_swagger_validator .
docker run --name swagger-validator -e APP_ADDR=0.0.0.0 -dp 7777:8000 python_swagger_validator
