import json
import logging

from notifier import DingTalkNotifier


def handler(environ, start_response):
    """
    FC index handler.
    """
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    if request_body:
        payload = json.loads(request_body)
        notifier = DingTalkNotifier(payload)
        try:
            notifier.notify()
        except Exception as e:
            logging.exception(e)
            return _response_failed(start_response, str(e))
    return _response_ok(start_response)


def _response(start_response, status, data):
    """
    Base response for WSGI.
    """
    response_body = json.dumps(data).encode('utf-8')
    response_headers = [
        ('Content-type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body]


def _response_ok(start_response):
    """
    Response ok.
    """
    status = '200 OK'
    ret = {'Success': True}
    return _response(start_response, status, ret)


def _response_failed(start_response, message):
    """
    Response failed.
    """
    status = '500 Internal Server Error'
    ret = {'Success': False, 'Message': message}
    return _response(start_response, status, ret)
