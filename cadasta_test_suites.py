#!/usr/bin/env python

import unittest

# Accounts
from selenium_tests.accounts.registration import (
    NewRegistration,
    RegistrationAttemptUsernameNotAvailable,
    RegistrationAttemptEmailNotAvailable
)
from selenium_tests.accounts.registration_form_validation import (
    PasswordValidation,
    ConfirmPasswordValidation,
    EmptyUsernameValidation,
    EmptyEmailValidation,
    EmptyPasswordValidation,
    EmptyConfirmPasswordValidation
)
from selenium_tests.accounts.login import (
    Login,
    LoginFailure
)
from selenium_tests.accounts.user_profile import (
    PasswordReset,
    PasswordChange,
    UsernameChange,
    FullnameChange,
    EmailChange
)

# Organizations
from selenium_tests.organizations.organization import (
    CreateOrganization,
    EditOrganization,
    OrganizationArchive
)
from selenium_tests.organizations.organization_search import (
    OrganizationSearch
)
from selenium_tests.organizations.organization_create_form_validation import (
    DuplicateOrganizationNameValidation,
    EmptyOrganizationNameValidation,
    OrganizationURLValidation
)
from selenium_tests.organizations.organization_members import (
    ViewMembers,
    ViewMemberProfile,
    AddMember,
    AddNonExistingMember,
    RemoveMember,
    SearchMembers
)

# Projects
from selenium_tests.projects.project import (
    CreatePublicProject,
    CreatePrivateProject,
    EditProjectDetails,
    ProjectAccessibility
)
from selenium_tests.projects.project_draw_on_map import (
    AddProjectWithExtent,
)
from selenium_tests.projects.search_project import (
    ProjectSearch
)
from selenium_tests.projects.project_resources import (
    AddResource
)
from selenium_tests.projects.project_location import (
    AddLocation,
    EditLocation,
    DeleteLocation
)
from selenium_tests.projects.location_resources import (
    AddLocationResource
)
from selenium_tests.projects.location_relationships import (
    AddLocationRelationship
)
from selenium_tests.projects.project_parties import (
    ViewParty,
    PartyResource,
    EditParty,
    DeleteParty
)


# Get all tests from accounts test classes
new_registration = unittest.TestLoader().loadTestsFromTestCase(NewRegistration)
registration_attempt_existing_username = unittest.TestLoader().loadTestsFromTestCase(RegistrationAttemptUsernameNotAvailable)
registration_attempt_existing_email = unittest.TestLoader().loadTestsFromTestCase(RegistrationAttemptEmailNotAvailable)
password_validation = unittest.TestLoader().loadTestsFromTestCase(PasswordValidation)
confirm_password_validation = unittest.TestLoader().loadTestsFromTestCase(ConfirmPasswordValidation)
empty_username_validation = unittest.TestLoader().loadTestsFromTestCase(EmptyUsernameValidation)
empty_email_validation = unittest.TestLoader().loadTestsFromTestCase(EmptyEmailValidation)
empty_password_validation = unittest.TestLoader().loadTestsFromTestCase(EmptyPasswordValidation)
empty_confirm_password_validation = unittest.TestLoader().loadTestsFromTestCase(EmptyConfirmPasswordValidation)
login_success = unittest.TestLoader().loadTestsFromTestCase(Login)
login_failure = unittest.TestLoader().loadTestsFromTestCase(LoginFailure)
password_reset = unittest.TestLoader().loadTestsFromTestCase(PasswordReset)
password_change = unittest.TestLoader().loadTestsFromTestCase(PasswordChange)
username_change = unittest.TestLoader().loadTestsFromTestCase(UsernameChange)
fullname_change = unittest.TestLoader().loadTestsFromTestCase(FullnameChange)
email_change = unittest.TestLoader().loadTestsFromTestCase(EmailChange)

# Get all tests from organizations test classes
create_organization = unittest.TestLoader().loadTestsFromTestCase(CreateOrganization)
edit_organization = unittest.TestLoader().loadTestsFromTestCase(EditOrganization)
archive_organization = unittest.TestLoader().loadTestsFromTestCase(OrganizationArchive)
search_organization = unittest.TestLoader().loadTestsFromTestCase(OrganizationSearch)
duplicate_org_name_validation = unittest.TestLoader().loadTestsFromTestCase(DuplicateOrganizationNameValidation)
empty_org_name_validation = unittest.TestLoader().loadTestsFromTestCase(EmptyOrganizationNameValidation)
org_url_validation = unittest.TestLoader().loadTestsFromTestCase(OrganizationURLValidation)
view_members = unittest.TestLoader().loadTestsFromTestCase(ViewMembers)
view_member_profile = unittest.TestLoader().loadTestsFromTestCase(ViewMemberProfile)
add_member = unittest.TestLoader().loadTestsFromTestCase(AddMember)
add_non_existing_member = unittest.TestLoader().loadTestsFromTestCase(AddNonExistingMember)
remove_member = unittest.TestLoader().loadTestsFromTestCase(RemoveMember)
search_member = unittest.TestLoader().loadTestsFromTestCase(SearchMembers)

# Get all tests from projects test classes
create_public_project = unittest.TestLoader().loadTestsFromTestCase(CreatePublicProject)
create_private_project = unittest.TestLoader().loadTestsFromTestCase(CreatePrivateProject)
edit_project_details = unittest.TestLoader().loadTestsFromTestCase(EditProjectDetails)
project_accessibility = unittest.TestLoader().loadTestsFromTestCase(ProjectAccessibility)
add_project_with_extent = unittest.TestLoader().loadTestsFromTestCase(AddProjectWithExtent)
project_search = unittest.TestLoader().loadTestsFromTestCase(ProjectSearch)
add_resource = unittest.TestLoader().loadTestsFromTestCase(AddResource)
add_location = unittest.TestLoader().loadTestsFromTestCase(AddLocation)
edit_location = unittest.TestLoader().loadTestsFromTestCase(EditLocation)
delete_location = unittest.TestLoader().loadTestsFromTestCase(DeleteLocation)
add_location_resource = unittest.TestLoader().loadTestsFromTestCase(AddLocationResource)
add_location_relationship = unittest.TestLoader().loadTestsFromTestCase(AddLocationRelationship)
view_party = unittest.TestLoader().loadTestsFromTestCase(ViewParty)
party_resources = unittest.TestLoader().loadTestsFromTestCase(PartyResource)
edit_party = unittest.TestLoader().loadTestsFromTestCase(EditParty)
delete_party = unittest.TestLoader().loadTestsFromTestCase(DeleteParty)


# Create Cadasta Accounts test suite
cadasta_accounts_test_suite = unittest.TestSuite([
    new_registration,
    registration_attempt_existing_username,
    registration_attempt_existing_email,
    password_validation,
    confirm_password_validation,
    empty_username_validation,
    empty_email_validation,
    empty_password_validation,
    empty_confirm_password_validation,
    password_reset,
    # password_change,
    username_change,
    fullname_change,
    email_change
])

# Create Cadasta Organizations test suite
cadasta_organizations_test_suite = unittest.TestSuite([
    create_organization,
    edit_organization,
    archive_organization,
    search_organization,
    duplicate_org_name_validation,
    empty_org_name_validation,
    org_url_validation,
    view_members,
    view_member_profile,
    add_member,
    add_non_existing_member,
    remove_member,
    search_member
])

# Create Cadasta Projects test suite
cadasta_projects_test_suite = unittest.TestSuite([
    create_public_project,
    create_private_project,
    edit_project_details,
    project_accessibility,
    add_project_with_extent,
    project_search,
    add_resource,
    add_location,
    edit_location,
    delete_location,
    add_location_resource,
    add_location_relationship,
    view_party,
    party_resources,
    edit_party,
    delete_party
])

# Run the suites
unittest.TextTestRunner(verbosity=2).run(cadasta_accounts_test_suite)
unittest.TextTestRunner(verbosity=2).run(cadasta_organizations_test_suite)
unittest.TextTestRunner(verbosity=2).run(cadasta_projects_test_suite)