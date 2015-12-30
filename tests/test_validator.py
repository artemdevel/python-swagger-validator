import json
import unittest

import responses
from webtest import TestApp

from app import create_app
from app import config
from tests.utils import (
    read_badge, VALID_JSON_SCHEMA, VALID_YAML_SCHEMA, INVALID_HTML_SCHEMA, INVALID_JSON_SCHEMA, INVALID_YAML_SCHEMA,
    DEPRECATED_SCHEMA)


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(create_app())

    def test_unknown_endpoint_fail(self):
        res = self.app.get('/unknown', expect_errors=True)
        self.assertEqual(res.status_int, 404)

    def test_index(self):
        res = self.app.get('/')
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.json, {'paths': ['/validator', '/validator/debug']})

    def test_validator_debug_json_ok(self):
        url = 'http://example.com/schema.json'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=VALID_JSON_SCHEMA, content_type='application/json')
            res = self.app.get('/validator/debug?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'application/json')
            self.assertEqual(res.json, 'OK')

    def test_validator_debug_yaml_ok(self):
        url = 'http://example.com/schema.yaml'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=VALID_YAML_SCHEMA, content_type='text/plain')
            res = self.app.get('/validator/debug?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'application/json')
            self.assertEqual(res.json, 'OK')

    def test_validator_debug_empty_url_fail(self):
        res = self.app.get('/validator/debug?url=')
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.json, "Can't read from file null")

    def test_validator_debug_not_found_url_fail(self):
        url = 'http://example.com/not_found.json'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=404)
            res = self.app.get('/validator/debug?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'application/json')
            self.assertEqual(res.json, "Can't read from file http://example.com/not_found.json")

    def test_validator_debug_spec_parse_fail(self):
        url = 'http://example.com/schema.html'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=INVALID_HTML_SCHEMA, content_type='text/html')
            res = self.app.get('/validator/debug?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'application/json')
            self.assertEqual(res.json, 'Unable to parse content. It may be invalid JSON or YAML')

    def test_validator_debug_deprecated_schema_fail(self):
        url = 'http://example.com/deprecated_schema.json'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=DEPRECATED_SCHEMA, content_type='application/json')
            res = self.app.get('/validator/debug?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'application/json')
            self.assertTrue('Deprecated Swagger version.' in res.json)

    def test_validator_debug_json_fail(self):
        url = 'http://example.com/invalid_schema.json'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=INVALID_JSON_SCHEMA, content_type='application/json')
            res = self.app.get('/validator/debug?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'application/json')
            self.assertTrue("'info' is a required property" in res.json)

    def test_validator_debug_yaml_fail(self):
        url = 'http://example.com/invalid_schema.yaml'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=INVALID_YAML_SCHEMA, content_type='text/plain')
            res = self.app.get('/validator/debug?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'application/json')
            self.assertTrue("'info' is a required property" in res.json)

    def test_validator_badge_json_ok(self):
        url = 'http://example.com/schema.json'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=VALID_JSON_SCHEMA, content_type='application/json')
            res = self.app.get('/validator?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'image/png')
            self.assertEqual(res.body, read_badge(config.VALID_BADGE))

    def test_validator_badge_yaml_ok(self):
        url = 'http://example.com/schema.yaml'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=VALID_YAML_SCHEMA, content_type='text/plain')
            res = self.app.get('/validator?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'image/png')
            self.assertEqual(res.body, read_badge(config.VALID_BADGE))

    def test_validator_badge_empty_url_fail(self):
        res = self.app.get('/validator?url=')
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'image/png')
        self.assertEqual(res.body, read_badge(config.INVALID_BADGE))

    def test_validator_badge_not_found_url_fail(self):
        url = 'http://example.com/not_found.json'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=404)
            res = self.app.get('/validator?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'image/png')
            self.assertEqual(res.body, read_badge(config.INVALID_BADGE))

    def test_validator_badge_spec_parse_fail(self):
        url = 'http://example.com/schema.html'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=INVALID_HTML_SCHEMA, content_type='text/html')
            res = self.app.get('/validator?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'image/png')
            self.assertEqual(res.body, read_badge(config.ERROR_BADGE))

    def test_validator_badge_deprecated_schema_fail(self):
        url = 'http://example.com/deprecated_schema.json'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=DEPRECATED_SCHEMA, content_type='application/json')
            res = self.app.get('/validator?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'image/png')
            self.assertEqual(res.body, read_badge(config.UPGRADE_BADGE))

    def test_validator_badge_json_fail(self):
        url = 'http://example.com/invalid_schema.json'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=INVALID_JSON_SCHEMA, content_type='application/json')
            res = self.app.get('/validator?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'image/png')
            self.assertEqual(res.body, read_badge(config.INVALID_BADGE))

    def test_validator_badge_yaml_fail(self):
        url = 'http://example.com/invalid_schema.yaml'
        with responses.RequestsMock() as res_req:
            res_req.add(responses.GET, url, status=200, body=INVALID_YAML_SCHEMA, content_type='text/plain')
            res = self.app.get('/validator?url={}'.format(url))
            self.assertEqual(res.status_int, 200)
            self.assertEqual(res.content_type, 'image/png')
            self.assertEqual(res.body, read_badge(config.INVALID_BADGE))

    def test_validator_debug_post_json_ok(self):
        res = self.app.post_json('/validator/debug', json.loads(VALID_JSON_SCHEMA))
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.json, 'OK')

    def test_validator_debug_post_deprecated_json_fail(self):
        res = self.app.post_json('/validator/debug', json.loads(DEPRECATED_SCHEMA))
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue('Deprecated Swagger version.' in res.json)

    def test_validator_debug_post_json_fail(self):
        res = self.app.post_json('/validator/debug', json.loads(INVALID_JSON_SCHEMA))
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'application/json')
        self.assertTrue("'info' is a required property" in res.json)

    def test_validator_debug_post_non_json_fail(self):
        res = self.app.post('/validator/debug', params=VALID_YAML_SCHEMA, content_type='text/html', expect_errors=True)
        self.assertEqual(res.status_int, 400)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.json['title'], 'Unsupported or missed content-type header')

    def test_validator_debug_post_malformed_json_fail(self):
        res = self.app.post(
            '/validator/debug', params=VALID_YAML_SCHEMA, content_type='application/json', expect_errors=True)
        self.assertEqual(res.status_int, 500)
        self.assertEqual(res.content_type, 'application/json')
        self.assertEqual(res.json['title'], 'Malformed JSON')


if __name__ == '__main__':
    unittest.main()
