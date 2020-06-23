#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019
#
# Distributed under terms of the MIT license.

from fnapy.utils import Message
from fnapy.fnapy_manager import FnapyManager
from fnapy.connection import FnapyConnection
from tests import make_requests_get_mock, fake_manager
from lxml import etree

try:
    from unittest import mock
except ImportError:
    import mock


def do_nothing(*args, **kwargs):
    pass


def test_query_messages(fake_manager):
    """
    We should be able to decode properly the messages we receive
    """
    # This example contains the subject 'Nouvelle réclamation'
    with mock.patch(
        'fnapy.fnapy_manager.FnapyManager._get_response',
        make_requests_get_mock('query_messages_response.xml')
    ):
        response = fake_manager.query_messages()

    # Once decoded in UTF-8, the xml string should contain the correct
    # characters.
    assert 'Nouvelle réclamation' in response.content.decode('utf8')


def test_update_messages(fake_manager):
    """
    The message we send should have the correct encoding
    """
    message1 = Message(
        action='mark_as_read',
        id=u'some_id',
        subject=u'order_information',
        description='Chère Valérià...'
    )
    with mock.patch(
        'fnapy.fnapy_manager.FnapyManager._get_response',
        side_effect=do_nothing
    ) as m:
        fake_manager.update_messages([message1])

    # The xml string passed to _get_response (called by update_messages) should
    # be encoded in UTF-8. Decoding it should give us the original message
    assert message1.description in m.call_args[0][1].decode('utf8')


def test_get_response_with_badly_encoded_bytes(fake_manager):
    """
    FnapyManager._get_response should return a correct `utils.Response` even if the raw
    bytes are not properly encoded in UTF8
    """
    xml_request = b"""
        <?xml version='1.0' encoding='utf-8'?>
        <messages_query xmlns="http://www.fnac.com/schemas/mp-dialog.xsd"
                        partner_id="X" shop_id="X" token="X"
                        results_count="100">
          <paging>1</paging>
        </messages_query>
    """
    # This example contains the subject 'Nouvelle réclamation'
    with mock.patch('fnapy.fnapy_manager.requests.post') as post:
        resp = make_requests_get_mock('query_messages_response.xml')()
        m = mock.Mock()
        # We purposely encode the body in ISO-8859-1 instead of UTF8
        m.content = resp.text.encode('ISO-8859-1')
        m.text = resp.text
        post.return_value = m
        response = fake_manager._get_response(
            etree.Element('messages_query'), xml_request
        )

    # Once decoded in UTF-8, the xml string should contain the correct
    # characters.
    assert 'Nouvelle réclamation' in response.xml.decode('utf8')
