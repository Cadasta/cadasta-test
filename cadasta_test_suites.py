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
    password_change,
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

# Run the suites
unittest.TextTestRunner(verbosity=2).run(cadasta_accounts_test_suite)
unittest.TextTestRunner(verbosity=2).run(cadasta_organizations_test_suite)