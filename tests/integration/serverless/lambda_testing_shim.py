import json

import cookbook.interfaces.lamdba as interface


# This feels insane?
class Mocker:
    def __init__(self, url):
        self.url = url

    def get(self, url, **kwargs):
        return self.mocker(url, 'get', **kwargs)

    def post(self, url, **kwargs):
        return self.mocker(url, 'post', **kwargs)

    def put(self, url, **kwargs):
        return self.mocker(url, 'put', **kwargs)

    def delete(self, url, **kwargs):
        return self.mocker(url, 'delete', **kwargs)

    # convert body to a string
    def mocker(self, url, method, **kwargs):
        path = url[len(self.url):]
        event = {
            'body': json.dumps(kwargs.get('json', {})),
            'requestContext': {
                'path': path
            }
        }

        # If path is /dev/cookbook, then want to list
        if method == 'get' and len(path.split('/')) == 1:
            method = 'list'
        fxn = getattr(interface, method)

        return self.Response(fxn(event, {}))

    class Response:
        def __init__(self, resp):
            self.status_code = resp.get('statusCode', 404)
            self.body = json.loads(resp.get('body', {}))

        def json(self):
            return self.body
