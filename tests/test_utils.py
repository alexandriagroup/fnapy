#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""
Tests for fnappy.utils module
"""

import os
from lxml import etree

from fnapy.utils import extract_text, findall, find
from fnapy.config import XHTML_NAMESPACE

NAMESPACES = {'ns': XHTML_NAMESPACE}


def parse_xml_file(filename):
     return etree.parse(os.path.join(os.path.dirname(__file__), 'assets', 
                                     filename))


def test_extract_text():
    """findall should return a list unique elements"""
    messages = parse_xml_file('messages_sample.xml')
    message_elements = messages.getroot().getchildren()
    # All the messages should have a different message_id
    message_ids = [extract_text(message_element, 'message_id') for
                   message_element in message_elements]
    assert len(set(message_ids)) == len(message_ids)


def test_find():
    """find should return an element"""
    messages = parse_xml_file('messages_sample.xml')
    message_id = find(messages, 'message/message_id').text
    first_message = messages.getroot().getchildren()[0]
    first_message_id = first_message.find('.//ns:message_id',
                                          namespaces=NAMESPACES).text
    assert message_id == first_message_id


def test_findall():
    """findall should return a list unique elements"""
    messages = parse_xml_file('messages_sample.xml')
    message_elements = findall(messages, 'message')
    message_ids = []
    for message_element in message_elements:
        message_id_element = message_element.find('.//ns:message_id',
                                                  namespaces=NAMESPACES)
        message_ids.append(message_id_element.text)
    assert len(set(message_ids)) == len(message_ids)
