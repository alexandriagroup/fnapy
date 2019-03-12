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


class FnapyUpdateOfferError(FnapyException):
    """Raised when the update of an offer is not valid"""


class FnapyUpdateOrderError(FnapyException):
    """Raised when the update of an order is not valid"""


class FnapyPricingError(FnapyException):
    """Raised when no prices is found when using pricing_query"""


class FnapyConnectionError(FnapyException):
    """Raised when the connection is incorrect"""


class FnapyResponseError(FnapyException):
    """Raised when the response is incorrect"""
