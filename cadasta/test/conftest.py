import json
import os
import pytest
import re

from datetime import datetime

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


@pytest.fixture(scope='session',
                params=['functest_org_member_',
                        'functest_data_collector_',
                        'functest_prj_user_'])
def any_non_pm_user(request, all_fixtures):
    return next(user for user in all_fixtures['accounts.user']
                if request.param in user['username'])


@pytest.fixture(scope='session',
                params=['functest_generic_',
                        'functest_genericphone_',
                        'functest_org_admin_',
                        'functest_org_member_',
                        'functest_prj_manager_',
                        'functest_data_collector_',
                        'functest_prj_user_'])
def any_user(request, all_fixtures):
    """
    This Pytest fixture function is intended for the user dashboard test and it
    provides the listed users in the params argument above one at a time to the
    test. For each user, the function extracts the corresponding organization,
    organization role, project, and project role information from the test
    fixtures and appends them to the user dict. The function also generates
    other roles such as administrator and public user project roles which are
    not explicitly represented in the database.

    The appended org and project data has the following structure:
    - list of org 3-tuples:
      - dict of core org data (straight from the fixture file)
      - bool of org admin role
      - list of project 2-tuples:
        - dict of core project data (straight from the fixture file)
        - 2-char string representing the project role (OA/PM/DC/PU/PB)
    """
    user = next(user for user in all_fixtures['accounts.user']
                if request.param in user['username'])

    # Convert string date-time into Python datetime object
    user['created_date'] = datetime.strptime(
        user['created_date'], '%Y-%m-%dT%H:%M:%S.000Z')

    # Collect orgs, projects, and roles for the user
    user['orgs'] = []
    for org_role in all_fixtures['organization.organizationrole']:
        if org_role['user'][0] != user['username']:
            continue
        for org in all_fixtures['organization.organization']:
            if org_role['organization'] != org['pk']:
                continue
            prj_data = []
            for prj in all_fixtures['organization.project']:
                if prj['organization'] != org['pk']:
                    continue
                if org_role['admin']:
                    prj_data.append((prj, 'OA'))
                    continue
                role_is_found = False
                for prj_role in all_fixtures['organization.projectrole']:
                    if prj_role['project'] != prj['pk']:
                        continue
                    if prj_role['user'][0] == user['username']:
                        prj_data.append((prj, prj_role['role']))
                        role_is_found = True
                if not role_is_found:
                    prj_data.append((prj, 'PB'))
            user['orgs'].append((org, org_role['admin'], prj_data))

    return user


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
    """
    This Pytest fixture function returns the dict corresponding to the Basic
    Prj with an additional key 'members' having a value which is a list of
    tuple of the project's members (users with project role in the project and
    users with an admin org role in the project's organization).

    The member tuple has the following structure:
    - dict of core user data (straight from the fixture file)
    - 2-char string representing the project role (OA/PM/DC/PU)
    """

    project = next(prj for prj in all_fixtures['organization.project']
                   if 'functest-basic-prj-' in prj['slug'])
    project['members'] = []

    # Extract non-org admins
    for prj_role in all_fixtures['organization.projectrole']:
        if prj_role['project'] != project['pk']:
            continue
        for user in all_fixtures['accounts.user']:
            if prj_role['user'][0] == user['username']:
                project['members'].append((user, prj_role['role']))

    # Extract org admins
    for org in all_fixtures['organization.organization']:
        if org['pk'] != project['organization']:
            continue
        for org_role in all_fixtures['organization.organizationrole']:
            if org_role['organization'] != org['pk'] or not org_role['admin']:
                continue
            for user in all_fixtures['accounts.user']:
                if org_role['user'][0] == user['username']:
                    project['members'].append((user, 'OA'))

    return project


@pytest.fixture(scope='session')
def private_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-private-prj-' in prj['slug'])


@pytest.fixture(scope='session')
def records_prj(all_fixtures):
    """This Pytest fixture function returns the dict corresponding to the
    Records Prj with statistics keys added."""
    project = next(prj for prj in all_fixtures['organization.project']
                   if 'functest-records-prj-' in prj['slug'])
    project['num_locations'] = len(
        [loc for loc in all_fixtures['spatial.spatialunit']
         if loc['project'] == project['pk']])
    project['num_parties'] = len(
        [party for party in all_fixtures['party.party']
         if party['project'] == project['pk']])
    project['num_resources'] = len(
        [res for res in all_fixtures['resources.resource']
         if res['project'] == project['pk']])
    return project


@pytest.fixture(scope='session')
def custom_attrs_prj(all_fixtures):
    """This Pytest fixture function returns the dict corresponding to the
    Custom Attrs Prj with an additional 'questionnaire' key added with a value
    corresponding to the questionnaire fixture data."""
    project = next(prj for prj in all_fixtures['organization.project']
                   if 'functest-custom-attrs-prj-' in prj['slug'])
    for questionnaire in all_fixtures['questionnaires.questionnaire']:
        if questionnaire['pk'] != project['current_questionnaire']:
            continue
        project['questionnaire'] = questionnaire
    return project


@pytest.fixture(scope='session')
def conditional_attrs_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-conditional-attrs-prj-' in prj['slug'])


@pytest.fixture(scope='session')
def custom_party_attrs_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-custom-party-attrs-prj-' in prj['slug'])


@pytest.fixture(scope='session')
def custom_tenure_attrs_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-custom-tenure-attrs-prj-' in prj['slug'])


@pytest.fixture(scope='session')
def custom_conditional_attrs_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-custom-conditional-attrs-prj-' in prj['slug'])


@pytest.fixture(scope='session')
def empty_prj(all_fixtures):
    return next(prj for prj in all_fixtures['organization.project']
                if 'functest-empty-prj-' in prj['slug'])


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


# Under FuncTest Records Prj
@pytest.fixture(scope='session')
def basic_parcel(all_fixtures):
    loc = next(location for location in all_fixtures['spatial.spatialunit']
               if 'xqzcnvuy7u9gywqkp2xa3rbn' == location['pk'])
    loc['type_label'] = 'Parcel'
    return loc


# Under FuncTest Custom Attrs Prj
@pytest.fixture(scope='session')
def custom_building(all_fixtures):
    loc = next(location for location in all_fixtures['spatial.spatialunit']
               if 'tcqrxxaep8jcf83xnynh6pxi' == location['pk'])
    loc['type_label'] = 'Building'
    return loc


# Under FuncTest Conditional Attrs Prj
@pytest.fixture(scope='session')
def basic_apartment(all_fixtures):
    loc = next(location for location in all_fixtures['spatial.spatialunit']
               if 'szcmfx455yt3r3q43thxk2mr' == location['pk'])
    loc['type_label'] = 'Apartment'
    return loc


# Under FuncTest Custom Party Attrs Prj
@pytest.fixture(scope='session')
def basic_rightofway(all_fixtures):
    loc = next(location for location in all_fixtures['spatial.spatialunit']
               if 'wdxgeavx3q95vmtr8xkyu2ac' == location['pk'])
    loc['type_label'] = 'Right-of-way'
    return loc


# Under FuncTest Custom Tenure Attrs Prj
@pytest.fixture(scope='session')
def basic_national_park(all_fixtures):
    loc = next(location for location in all_fixtures['spatial.spatialunit']
               if 'sq8nvq4syhy7zdf4tsrwia54' == location['pk'])
    loc['type_label'] = 'National Park Boundary'
    return loc


# Under FuncTest Custom-Conditional Attrs Prj
@pytest.fixture(scope='session')
def basic_community_boundary(all_fixtures):
    loc = next(location for location in all_fixtures['spatial.spatialunit']
               if 'zw27euyqjmvnvxfedh4s7qae' == location['pk'])
    loc['type_label'] = 'Community Boundary'
    return loc


# Under FuncTest Records Prj
@pytest.fixture(scope='session')
def basic_individual(all_fixtures):
    return next(party for party in all_fixtures['party.party']
                if 'Basic Individual' == party['name'])


# Under FuncTest Custom Tenure Attrs Prj
@pytest.fixture(scope='session')
def basic_group(all_fixtures):
    return next(party for party in all_fixtures['party.party']
                if 'Basic Group' == party['name'])


# Under FuncTest Records Prj
@pytest.fixture(scope='session')
def basic_water_rights(all_fixtures, basic_parcel, basic_individual):
    tenure_rel = next(rel for rel in all_fixtures['party.tenurerelationship']
                      if 'yku4hjxu5rka882n84jyw5wj' == rel['pk'])
    tenure_rel['location'] = basic_parcel
    tenure_rel['party'] = basic_individual
    tenure_rel['type_label'] = 'Water Rights'
    return tenure_rel


# Under FuncTest Records Prj
@pytest.fixture(scope='session')
def dummy_resource_1(all_fixtures):
    resource = next(res for res in all_fixtures['resources.resource']
                    if 'FuncTest Dummy Resource 1' == res['name'])
    resource['type'] = re.split('\.', resource['original_file'])[-1]
    # Convert string date-time into Python datetime object
    resource['last_updated'] = datetime.strptime(
        resource['last_updated'], '%Y-%m-%dT%H:%M:%S.000Z')
    return resource


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
