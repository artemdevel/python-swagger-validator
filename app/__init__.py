import json

import falcon
from structlog import get_logger

from app import config
from app.validator.handlers import ValidatorBadgeHandler, ValidatorDebugHandler

log = get_logger()


class JSONResponse:
    def process_response(self, req, res, resource):
        if res.content_type is None:
            res.content_type = 'application/json'
            res.body = json.dumps(res.body, indent=4, separators=(',', ': '))
            return


class IndexHandler:
    def on_get(self, req, res):
        """
        @type req: falcon.Request
        @type res: falcon.Response
        """
        res.body = {'paths': ['/validator', '/validator/debug']}


def create_app():
    log.info('Starting {}'.format(config.APP_NAME))
    app = falcon.API(middleware=[JSONResponse()])
    app.add_route('/', IndexHandler())
    app.add_route('/validator', ValidatorBadgeHandler())
    app.add_route('/validator/debug', ValidatorDebugHandler())
    return app
