#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""
Exceptions in fnapy
"""


class FnapyException(Exception):
    """Main exception class"""
    pass


class FnapyUpdateOfferError(FnapyException):
    """Raised when the update of an offer is not valid"""
    pass


class FnapyPricingError(FnapyException):
    """Raised when no prices is found when using pricing_query"""
    pass


class FnapyConnectionError(FnapyException):
    """Raised when the connection is incorrect"""
    pass
