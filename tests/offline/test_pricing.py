#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

# Python modules
from __future__ import unicode_literals

# Project modules
from tests import fake_manager
from tests.offline import create_context_for_requests
from fnapy.config import XHTML_NAMESPACE


def test_query_pricing(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'query_pricing', 'pricing_query')
    with context:
        fake_manager.query_pricing(
            [
                {'value': '9780262510875', 'type': 'Ean'},
                {'value': '2359109693', 'type': 'Isbn'},
                {'value': '8172119', 'type': 'FnacId'},
            ]
        )


# This time, we must also test the response because it may contain an error we
def test_query_pricing_with_invalid_ean(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'query_pricing_with_invalid_ean',
                                          'pricing_query')
    with context:
        response = fake_manager.query_pricing(['007'])
        errors = response.element.xpath('//ns:error',
                                        namespaces={'ns': XHTML_NAMESPACE})
        assert len(errors) != 0


def test_query_pricing_with_invalid_code_type(monkeypatch, fake_manager):
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'query_pricing_with_invalid_code_type',
                                          'pricing_query')
    with context:
        response = fake_manager.query_pricing(
            [
                {'value': '9780262510875', 'type': 'X'},
                {'value': '2359109693', 'type': 'Isbn'},
                {'value': '8172119', 'type': 'FnacId'},
            ]
        )
        errors = response.element.xpath('//ns:error',
                                        namespaces={'ns': XHTML_NAMESPACE})
        assert len(errors) != 0


def test_query_pricing_with_more_than_ten_eans(monkeypatch, fake_manager):
    """query_pricing should display an error message and return the error
    response when more that 10 EANs are passed"""
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'query_pricing_more_than_ten_eans',
                                          'pricing_query')
    with context:
        response = fake_manager.query_pricing(['007']*11)
        errors = response.element.xpath('//ns:error',
                                        namespaces={'ns': XHTML_NAMESPACE})
        assert len(errors) == 1


def test_query_pricing_with_no_ean(monkeypatch, fake_manager):
    """query_pricing should display an error message and return the error
    response when more there no EANs are passed"""
    context = create_context_for_requests(monkeypatch, fake_manager,
                                          'query_pricing_with_no_ean',
                                          'pricing_query')
    with context:
        response = fake_manager.query_pricing([])
        errors = response.element.xpath('//ns:error',
                                        namespaces={'ns': XHTML_NAMESPACE})
        assert len(errors) == 1
