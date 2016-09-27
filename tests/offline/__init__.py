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


@contextmanager
def create_context_for_requests(monkeypatch, manager, action, service, test_request=True):
    monkeypatch.setattr('requests.post', make_requests_get_mock(action + '_response.xml'))
    try:
        yield manager
    except Exception as e:
        pytest.fail(e.message)
    # if request is None, this means something went wrong.
    # This may be an exception raised in the call of a method
    request = getattr(manager, service + '_request')
    assert request_is_valid(request, action, service)
    


