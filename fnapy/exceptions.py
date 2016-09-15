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


class FnapyPricingError(FnapyException):
    """Raised when no prices is found when using pricing_query"""
    pass 
