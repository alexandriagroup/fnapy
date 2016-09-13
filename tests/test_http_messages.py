#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""
Test the Request and Response classes
"""

from fnapy.utils import Response, Request
from lxml import etree
from fnapy.utils import xml2dict, remove_namespace
from tests import elements_are_equal


BATCH_ID = "BFACA5F5-67FD-C037-6209-F287800FBB17"


def test_request():
    xml_request = """<?xml version='1.0' encoding='utf-8'?>
<batch_status xmlns="http://www.fnac.com/schemas/mp-dialog.xsd" partner_id="X" shop_id="X" token="X"><batch_id>{}</batch_id></batch_status>
    """.format(BATCH_ID)

    xml_request = remove_namespace(xml_request)
    request = Request(xml_request)
    element = etree.Element('batch_status', partner_id='X', shop_id='X', token='X')
    etree.SubElement(element, 'batch_id').text = BATCH_ID
    
    assert request.dict == xml2dict(xml_request)
    assert request.xml == xml_request
    assert request.tag == 'batch_status'
    assert elements_are_equal(request.element, element)


def test_response():
    xml_response = """<?xml version="1.0" encoding="utf-8"?>
<offers_update_response status="OK" xmlns="http://www.fnac.com/schemas/mp-dialog.xsd"><batch_id>{}</batch_id></offers_update_response>
    """.format(BATCH_ID)

    xml_response = remove_namespace(xml_response)
    response = Response(xml_response)
    element = etree.Element('offers_update_response', status='OK')
    etree.SubElement(element, 'batch_id').text = BATCH_ID
    
    assert response.dict == xml2dict(xml_response)
    assert response.xml == xml_response
    assert response.tag == 'offers_update_response'
    assert elements_are_equal(response.element, element)


