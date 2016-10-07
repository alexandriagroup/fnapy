# Python modules
from datetime import datetime

# Third-party modules
import pytz

# Project modules
from fnapy.utils import Query


def test_query():
    """Query(name) should generate a valid request"""
    date = Query('date')
    _dict = date.dict
    assert len(_dict) == 0

def test_query_with_attributes():
    """Query(name, type=type) should generate a valid request"""
    date = Query('date', type='CreatedAt')
    _dict = date.dict
    assert len(_dict) == 1
    assert _dict.get('@type') == 'CreatedAt'

def test_query_between():
    """Query(name, type=type).between(min=dmin, max=dmax) should generate a valid request"""
    dmin = datetime(2016, 8, 23, 0, 0, 0).replace(tzinfo=pytz.utc).isoformat()
    dmax = datetime(2016, 9, 2, 0, 0, 0).replace(tzinfo=pytz.utc).isoformat()
    date = Query('date', type='CreatedAt')
    _dict = date.between(min=dmin, max=dmax).dict

    # Assert the number of keys is correct
    assert len(_dict) == 3

    # Assert the keys are correct
    assert _dict.get('@type') == 'CreatedAt'
    assert _dict.get('min', {}).get('#text') == dmin
    assert _dict.get('max', {}).get('#text') == dmax

    # Assert the order of the keys is preserverd
    assert list(_dict) == ['@type', 'min', 'max']

def test_query_was():
    """Query('state').was(state) should generate a valid request"""
    states = Query('state').was('Created')
    _dict = states.dict

    # Assert the number of keys is correct
    assert len(_dict) == 1

    # Assert the keys are correct
    assert _dict.get('state', {}).get('#text') == 'Created'
