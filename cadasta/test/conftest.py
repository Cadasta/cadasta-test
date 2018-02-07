import json
import os
import pytest

from .webdriver import CustomWebDriver


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
            if 'pk' in datum:
                datum['fields']['pk'] = datum['pk']
            if datum['model'] == 'accounts.user':
                datum['fields']['password'] = DEFAULT_PASSWORD
            fixtures[datum['model']].append(datum['fields'])
    return fixtures


@pytest.fixture(scope='session')
def generic_user(all_fixtures):
    return next(user for user in all_fixtures['accounts.user']
                if 'functest_generic_' in user['username'])


@pytest.fixture(scope='session')
def generic_phone_user(all_fixtures):
    return next(user for user in all_fixtures['accounts.user']
                if 'functest_genericphone_' in user['username'])


@pytest.fixture(scope='session')
def org_creator(all_fixtures):
    return next(user for user in all_fixtures['accounts.user']
                if 'functest_org_creator_' in user['username'])


@pytest.fixture(scope='session')
def org_admin(all_fixtures):
    return next(user for user in all_fixtures['accounts.user']
                if 'functest_org_admin_' in user['username'])


@pytest.fixture(scope='session')
def org_member(all_fixtures):
    return next(user for user in all_fixtures['accounts.user']
                if 'functest_org_member_' in user['username'])


@pytest.fixture(scope='session')
def prj_manager(all_fixtures):
    return next(user for user in all_fixtures['accounts.user']
                if 'functest_prj_manager_' in user['username'])


@pytest.fixture(scope='session')
def data_collector(all_fixtures):
    return next(user for user in all_fixtures['accounts.user']
                if 'functest_data_collector_' in user['username'])


@pytest.fixture(scope='session')
def prj_user(all_fixtures):
    return next(user for user in all_fixtures['accounts.user']
                if 'functest_prj_user_' in user['username'])


@pytest.fixture(scope='session',
                params=['functest_org_admin_', 'functest_org_member_'])
def any_org_member(request, all_fixtures):
    return next(user for user in all_fixtures['accounts.user']
                if request.param in user['username'])


@pytest.fixture(scope='session')
def basic_org(all_fixtures):
    return next(org for org in all_fixtures['organization.organization']
                if 'functest-basic-org-' in org['slug'])


@pytest.fixture(scope='session')
def another_org(all_fixtures):
    return next(org for org in all_fixtures['organization.organization']
                if 'functest-another-org-' in org['slug'])


@pytest.fixture(scope='session')
def archivable_org(all_fixtures):
    return next(org for org in all_fixtures['organization.organization']
                if 'functest-archivable-org-' in org['slug'])


@pytest.fixture(scope='session')
def basic_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-basic-prj-' in prj['slug'])


@pytest.fixture(scope='session')
def private_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-private-prj-' in prj['slug'])


@pytest.fixture(scope='session')
def records_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-records-prj-' in prj['slug'])


@pytest.fixture(scope='session')
def custom_attrs_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-custom-attrs-prj-' in prj['slug'])


@pytest.fixture(scope='session')
def conditional_attrs_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-conditional-attrs-prj-' in prj['slug'])


@pytest.fixture(scope='session')
def another_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-another-prj-' in prj['slug'])


@pytest.fixture(scope='session')
def all_org_members(all_fixtures, basic_org):
    """Returns the list of fixture data corresponding to the members of the
       basic organization, with an extra field 'admin'."""
    roles = {role['user'][0]: role['admin']
             for role in all_fixtures['organization.organizationrole']
             if role['organization'] == basic_org['pk']}
    assert len(roles.keys()) > 0
    usernames = roles.keys()
    members = []
    for user in all_fixtures['accounts.user']:
        if user['username'] in usernames:
            user['admin'] = roles[user['username']]
            members.append(user)
    return members


@pytest.fixture(scope='session')
def basic_individual(all_fixtures):
    return next(party for party in all_fixtures['party.party']
                if 'Basic Individual' == party['name'])


@pytest.fixture(scope='session')
def basic_parcel(all_fixtures):
    return next(location for location in all_fixtures['spatial.spatialunit']
                if 'xqzcnvuy7u9gywqkp2xa3rbn' == location['pk'])


@pytest.fixture
def webdriver():

    # Initialize webdriver
    webdriver_option = os.environ.get('CADASTA_TEST_WEBDRIVER', 'Chrome')
    if 'BrowserStack' in webdriver_option:
        url = 'http://{}:{}@hub.browserstack.com:80/wd/hub'.format(
            os.environ.get('BROWSERSTACK_USERNAME'),
            os.environ.get('BROWSERSTACK_ACCESS_KEY'))
        local_identifier = os.environ.get('BROWSERSTACK_LOCAL_IDENTIFIER')
        caps = {
            'os': 'Windows',
            'os_version': '10',
            'browser': 'Chrome',
            'browserstack.local': 'true',
            'browserstack.localIdentifier': local_identifier,
            'resolution': '1920x1080',
        }
        wd = CustomWebDriver(command_executor=url, desired_capabilities=caps)
    else:
        wd = CustomWebDriver()

    # Provide the webdriver fixture
    yield wd

    # Shut down the webdriver
    wd.quit()
