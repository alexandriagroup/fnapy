#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

# Python modules
from __future__ import unicode_literals

# Third-party modules
import pytest

# Project modules
from fnapy.exceptions import FnapyPricingError
from tests import make_requests_get_mock, fake_manager
from tests.offline import create_context_for_requests


def test_query_pricing(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
            'query_pricing', 'pricing_query')
    with context:
        eans = [7321900286480, 9780262510875, 5060314991222]
        fake_manager.query_pricing(eans=eans)


# This time, we must also test the response because it may contain an error we
# want to catch and raise a FnapyPricingError
def test_query_pricing_with_invalid_ean(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
            'query_pricing_with_invalid_ean',
            'pricing_query')
    with context:
        with pytest.raises(FnapyPricingError):
            fake_manager.query_pricing(eans=['007'])
