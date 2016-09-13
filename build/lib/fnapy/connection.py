#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""
The class storing all the information for the connection to the FNAC API
"""


class FnapyConnection(object):
    def __init__(self, partner_id, shop_id, key):
        self.partner_id = partner_id
        self.shop_id = shop_id
        self.key = key
        

