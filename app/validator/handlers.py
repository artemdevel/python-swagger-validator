import json
import yaml

import falcon
import requests
from structlog import get_logger
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from app import config

log = get_logger()


def swagger_validator(url):
    """ Download Swagger schema and validate it against Swagger specification stored in assets/ folder.
        Return check result as a tuple of message and badge image name.
    """
    if url is None:
        return "Can't read from file null", config.INVALID_BADGE

    spec_req = requests.get(url)
    if spec_req.status_code != 200:
        return "Can't read from file {}".format(url), config.INVALID_BADGE

    try:
        if spec_req.headers['content-type'] == 'application/json':
            spec_body = json.loads(spec_req.text)
        else:
            spec_body = json.loads(json.dumps(yaml.load(spec_req.text)))

        version = spec_body['swagger']
        if version.startswith('1'):
            return (
                'Deprecated Swagger version. Please visit http://swagger.io '
                'for information on upgrading to Swagger 2.0', config.UPGRADE_BADGE)
    except (ValueError, KeyError):
        return 'Unable to read content. It may be invalid JSON or YAML', config.ERROR_BADGE

    with open(config.JSON_SCHEMA) as schema:
        swagger_schema = json.loads(schema.read())

    try:
        validate(spec_body, swagger_schema)
    except ValidationError as ex:
        return str(ex), config.INVALID_BADGE

    return 'OK', config.VALID_BADGE


class ValidatorBadgeHandler:
    def on_get(self, req, res):
        """
        @type req: falcon.Request
        @type res: falcon.Response
        """
        res.status = falcon.HTTP_200
        res.cache_control = ["no-cache"]
        res.content_type = "image/png"

        _, badge = swagger_validator(req.params.get('url'))
        with open(badge, "rb") as badge:
            res.body = badge.read()


class ValidatorDebugHandler:
    def on_get(self, req, res):
        """
        @type req: falcon.Request
        @type res: falcon.Response
        """
        res.status = falcon.HTTP_200
        res.cache_control = ["no-cache"]

        result, _ = swagger_validator(url=req.params.get('url'))
        res.body = result
