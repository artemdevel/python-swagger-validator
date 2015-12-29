VALID_JSON_SCHEMA = """
{
    "swagger": "2.0",
    "info": {"title": "Mini API", "version": "1.0.0"},
    "host": "example.com",
    "basePath": "/api",
    "schemes": ["https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "paths": {
        "/items": {
            "get": {
                "description": "Returns list of items.",
                "responses": {
                    "200": {
                        "description": "A list of items.",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/Item"
                            }
                        }
                    }
                }
            }
        }
    },
    "definitions": {
        "Item": {
            "type": "object",
            "required": ["id", "title"],
            "properties": {
                    "id": {"type": "integer", "format": "int64"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        }
    }
"""

VALID_YAML_SCHEMA = """
swagger: "2.0"
info:
  version: 1.0.0
  title: Mini API
host: example.com
basePath: /api
schemes:
  - https
consumes:
  - application/json
produces:
  - application/json
paths:
  /items:
    get:
      summary: Returns list of items.
      responses:
        200:
          description: A list of items.
          schema:
            type: array
            items:
              $ref: '#/definitions/Item'
definitions:
  Item:
    required:
      - id
      - title
    properties:
      id:
        type: integer
        format: int64
      title:
        type: string
      description:
        type: string
"""

DEPRECATED_SCHEMA = """
{
    "swagger": "1.2",
    "info": {"title": "Mini API", "version": "1.0.0"},
    "host": "example.com",
    "basePath": "/api",
    "schemes": ["https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "paths": {
        "/items": {
            "get": {
                "description": "Returns list of items.",
                "responses": {
                    "200": {
                        "description": "A list of items.",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/Item"
                            }
                        }
                    }
                }
            }
        }
    },
    "definitions": {
        "Item": {
            "type": "object",
            "required": ["id", "title"],
            "properties": {
                    "id": {"type": "integer", "format": "int64"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        }
    }
"""

INVALID_HTML_SCHEMA = """
<!DOCTYPE html>
<html lang="en" class=" is-copy-enabled">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="Content-Language" content="en">
    <meta name="viewport" content="width=1020">"""

INVALID_JSON_SCHEMA = """
{
    "swagger": "2.0",
    "host": "example.com",
    "basePath": "/api",
    "schemes": ["https"],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "paths": {
        "/items": {
            "get": {
                "description": "Returns list of items.",
                "responses": {
                    "200": {
                        "description": "A list of items.",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/Item"
                            }
                        }
                    }
                }
            }
        }
    },
    "definitions": {
        "Item": {
            "type": "object",
            "required": ["id", "title"],
            "properties": {
                    "id": {"type": "integer", "format": "int64"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                }
            }
        }
    }
"""

INVALID_YAML_SCHEMA = """
swagger: "2.0"
host: example.com
basePath: /api
schemes:
  - https
consumes:
  - application/json
produces:
  - application/json
paths:
  /items:
    get:
      summary: Returns list of items.
      responses:
        200:
          description: A list of items.
          schema:
            type: array
            items:
              $ref: '#/definitions/Item'
definitions:
  Item:
    required:
      - id
      - title
    properties:
      id:
        type: integer
        format: int64
      title:
        type: string
      description:
        type: string
"""


def read_badge(badge_path):
    with open(badge_path, "rb") as badge:
        return badge.read()
