# coding: utf-8
from __future__ import unicode_literals, print_function
import os
import pytest

from codecs import open
from contextlib import contextmanager

from requests import Response


def make_requests_get_mock(filename):
    def mockreturn(*args, **kwargs):
        response = Response()
        with open(os.path.join(os.path.dirname(__file__), 'Assets', filename), 'r', 'ISO-8859-1') as fd:
            response._content = fd.read().encode('utf-8')
        return response
    return mockreturn


def make_simple_text_mock(filename):
    def mockreturn(*args, **kwargs):
        with open(os.path.join(os.path.dirname(__file__), 'Assets', filename), 'r', 'ISO-8859-1') as fd:
            return fd.read()
    return mockreturn


@contextmanager
def assert_raises(exception_class, msg=None):
    """Check that an exception is raised and its message contains `msg`."""
    with pytest.raises(exception_class) as exception:
        yield
    if msg is not None:
        message = '%s' % exception
        assert msg.lower() in message.lower()
