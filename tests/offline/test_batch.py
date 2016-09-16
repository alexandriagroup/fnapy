# Python modules
from __future__ import unicode_literals

# Third-party modules
import pytest

# Project modules
from tests import fake_manager
from tests.offline import create_context_for_requests


def test_get_batch_status(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'get_batch_status', 'batch_status')
    with context:
        fake_manager.get_batch_status('5D239E08-F6C1-8965-F2FA-7EFCC9E7BAD1')


def test_query_batch(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'query_batch', 'batch_query')
    with context:
        fake_manager.query_batch()
