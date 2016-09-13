# coding: utf-8

# Python modules
from __future__ import unicode_literals, print_function
import os
from codecs import open
from contextlib import contextmanager

# Third-party modules
import pytest

# Project modules
from requests import Response
from tests import request_is_valid


def make_requests_get_mock(filename):
    def mockreturn(*args, **kwargs):
        response = Response()
        with open(os.path.join(os.path.dirname(__file__), '../assets', filename), 'r', 'utf-8') as fd:
            response._content = fd.read().encode('utf-8')
        return response
    return mockreturn


class ContextualTest(object):
    def __init__(self, monkeypatch, manager, action, service):
        self.manager = manager
        self.action = action
        self.service = service
        monkeypatch.setattr('requests.post', make_requests_get_mock(self.action + '_response.xml'))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        request = getattr(self.manager, self.service + '_request')
        print('%s, %s, %s' % (exc_type, exc_val, exc_tb))
        assert request_is_valid(request, self.action, self.service)
        return True

