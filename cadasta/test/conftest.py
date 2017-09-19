import json
import os
import pytest


DEFAULT_PASSWORD = 'XYZ#qwerty'


@pytest.fixture(scope='session')
def all_fixtures():
    """This is a master fixture function that loads the Django loaddata test
    fixtures and provides them as queryable dicts for secondary fixture
    functions."""

    # Load the JSON files
    fixtures = {}
    dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    files = [os.path.join(dir, f) for f in os.listdir(dir) if '.json' in f]
    for f in files:
        for datum in json.load(open(f)):
            if datum['model'] not in fixtures:
                fixtures[datum['model']] = []
            if datum['model'] == 'accounts.user':
                datum['fields']['password'] = DEFAULT_PASSWORD
            fixtures[datum['model']].append(datum['fields'])
    return fixtures


@pytest.fixture(scope='session')
def generic_user(all_fixtures):
    return next(item for item in all_fixtures['accounts.user']
                if 'functest_generic' in item['username'])
