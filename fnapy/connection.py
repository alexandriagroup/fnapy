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

from fnapy.exceptions import FnapyConnectionError
from fnapy.utils import get_credentials


def check_credentials_validity(credentials):
    invalid_credentials = []
    for k, v in credentials.items():
        if v is None:
            invalid_credentials.append(k)

    if len(invalid_credentials):
        msg = 'These credentials are invalid: '
        msg += ', '.join(invalid_credentials)
        raise FnapyConnectionError(msg)


class FnapyConnection(object):
    """The connection class of fnapy

    Usage::
        connection = FnapyConnection(credentials=credentials, sandbox=sandbox)

    Example:

    * Create a connection with a credentials dictionary::

        credentials = {'partner_id': 'my_partner_id', 'shop_id': 'my_shop_id',
                       'key': 'my_key', 'sandbox': False}

    * Create a connection using the environment variables for a given account
      type (the sandbox account is used if sandbox True. If sandbox is False, the
      real account is used)::

        connection = FnapyConnection(sandbox=True)

    .. note:: You must have previously defined the following environment
        variables:

    * for the sandbox: FNAC_SANDBOX_PARTNER_ID, FNAC_SANDBOX_SHOP_ID,
        FNAC_SANDBOX_KEY

    * for the real account: FNAC_PARTNER_ID, FNAC_SHOP_ID, FNAC_KEY

    """
    def __init__(self, credentials={}, sandbox=None):
        # credentials
        if len(credentials) > 0:
            expecteds = ('partner_id', 'shop_id', 'key', 'sandbox')
            for expected in expecteds:
                if credentials.get(expected) is None:
                    msg = "You didn't provide the {}."
                    msg += 'You must provide the following keys in credentials: '
                    msg += ', '.join(expecteds)
                    raise FnapyConnectionError(msg.format(expected))

        # sandbox
        else:
            if sandbox is not None:
                credentials = get_credentials(sandbox)
                credentials.update({'sandbox': sandbox})
            else:
                msg = 'You must either specify credentials or sandbox as arguments.'
                raise FnapyConnectionError(msg)

        check_credentials_validity(credentials)
        self.partner_id = credentials['partner_id']
        self.shop_id = credentials['shop_id']
        self.key = credentials['key']
        self.sandbox = credentials['sandbox']
