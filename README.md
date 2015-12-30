# python-swagger-validator
Python implementation of [Swagger validator-badge service](https://github.com/swagger-api/validator-badge)

The code was developed to work under Python 3.

This project tries to be compatible with the original project but there are some differences in error messages
because different JSON Schema validation libraries are used. Also error messages are represented as strings instead
of a list of objects as in the original implementation.

# Run locally

    ./run_app.py

By default the application is served on 127.0.0.1:8000 but this can be changed by setting environment variables
`APP_ADDR` and `APP_PORT` respectively.

# Run tests

    python -m unittest -v

# Run inside a Docker container

    docker build -t python-swagger .
    docker run --name swagger-validator -dp 8000:8000 python-swagger
    docker run --name swagger-validator -dp 127.0.0.1:8000:8000 python-swagger
    docker run --name swagger-validator -e APP_ADDR=0.0.0.0 -dp 127.0.0.1:8000:8000 python-swagger

NOTE: it doesn't have sense to override a port number for the application inside a container because it can be
overridden via docker command line parameters, but the application address must be overridden because by default it is
127.0.0.1 and the application won't be available outside the container.
