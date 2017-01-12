from functional_tests.selenium_tests.tests.accounts.registration import (
    NewRegistration,
    RegistrationAttemptUsernameNotAvailable,
    RegistrationAttemptEmailNotAvailable
)
from functional_tests.selenium_tests.tests.accounts.registration_form_validation import (
    PasswordValidation,
    ConfirmPasswordValidation,
    EmptyUsernameValidation,
    EmptyEmailValidation,
    EmptyPasswordValidation,
    EmptyConfirmPasswordValidation
)
from functional_tests.selenium_tests.tests.accounts.login import (
    Login,
    LoginFailure
)
from functional_tests.selenium_tests.tests.accounts.user_profile import (
    PasswordReset,
    PasswordChange,
    UsernameChange,
    FullnameChange,
    EmailChange
)
from functional_tests.selenium_tests.tests.organizations.organization import (
    CreateOrganization,
    EditOrganization,
    OrganizationArchive
)
from functional_tests.selenium_tests.tests.organizations.organization_search import (
    OrganizationSearch
)
from functional_tests.selenium_tests.tests.organizations.organization_create_form_validation import (
    DuplicateOrganizationNameValidation,
    EmptyOrganizationNameValidation,
    OrganizationURLValidation
)
from functional_tests.selenium_tests.tests.organizations.organization_members import (
    ViewMembers,
    ViewMemberProfile,
    AddMember,
    AddNonExistingMember,
    RemoveMember,
    SearchMembers
)
from functional_tests.selenium_tests.tests.projects.project import (
    CreateProject,
    EditProject
)
