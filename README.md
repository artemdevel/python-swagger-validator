# python-swagger-validator
Python implementation of [Swagger validator-badge service](https://github.com/swagger-api/validator-badge)

The code was developed to work under Python 3.

This project tries to be compatible with the original project but there are some differences in error messages
because different JSON Schema validation libraries are used. Also error messages are represented as strings instead
of a list of objects as in the original implementation.

Run tests `python -m unittest -v`
