#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016  <>
#
# Distributed under terms of the MIT license.

"""
Tests for FnapyConnection
"""

# Python imports
import os

# Third-party imports
import pytest

# fnapy imports
from fnapy.connection import FnapyConnection
from fnapy.exceptions import FnapyConnectionError


def mock_get_env_vars(env_vars_exists):
    """Mock the call to os.getenv in get_credentials"""

    expecteds = ('partner_id', 'shop_id', 'key', 'sandbox')
    credentials = dict().fromkeys(expecteds)

    if env_vars_exists:
        for expected in expecteds:
            credentials.update({expected: 'XXX'})
    return credentials


def test_connection_with_available_env_vars_for_sandbox(monkeypatch):
    """FnapyConnection should be able to accept the keyword sandbox=True when env vars exist"""
    monkeypatch.setattr('fnapy.connection.get_credentials', lambda x: mock_get_env_vars(True))
    connection = FnapyConnection(sandbox=True)


def test_connection_with_available_env_vars_for_real_account(monkeypatch):
    """FnapyConnection should be able to accept the keyword sandbox=False when env vars exist"""
    monkeypatch.setattr('fnapy.connection.get_credentials', lambda x: mock_get_env_vars(True))
    connection = FnapyConnection(sandbox=False)


def test_connection_with_unavailable_env_vars_for_sandbox(monkeypatch):
    """FnapyConnection should raise a FnapyConnectionError when sandbox=True and env vars don't exist"""
    monkeypatch.setattr('fnapy.connection.get_credentials', lambda x: mock_get_env_vars(False))
    with pytest.raises(FnapyConnectionError):
        connection = FnapyConnection(sandbox=True)


def test_connection_with_unavailable_env_vars_for_real_account(monkeypatch):
    """FnapyConnection should raise a FnapyConnectionError when sandbox=False and env vars don't exist"""
    monkeypatch.setattr('fnapy.connection.get_credentials', lambda x: mock_get_env_vars(False))
    with pytest.raises(FnapyConnectionError):
        connection = FnapyConnection(sandbox=False)


def test_connection_with_valid_keys_for_credentials():
    """FnapyConnection should be able to accept a dict with valid keys for the credentials"""
    credentials = {'partner_id': 'abc', 'shop_id': 'thebestshop',
                   'key': 'goldenkey', 'sandbox': False}
    connection = FnapyConnection(credentials=credentials)


def test_connection_with_invalid_keys_for_credentials():
    """FnapyConnection should raise a FnapyConnectionError if an invalid key is provided"""
    credentials = {'login': 'abc', 'shop_id': 'thebestshop',
                   'key': 'goldenkey', 'sandbox': True}
    with pytest.raises(FnapyConnectionError):
        connection = FnapyConnection(credentials=credentials)


def test_connection_with_credentials_and_sandbox():
    """credentials should supersede sandbox"""
    credentials = {'partner_id': 'abc', 'shop_id': 'thebestshop',
                   'key': 'goldenkey', 'sandbox': True}
    sandbox = False
    connection = FnapyConnection(credentials, sandbox)
    for k, v in credentials.items():
        assert getattr(connection, k) == v

