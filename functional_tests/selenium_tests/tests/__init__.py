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
    CreatePublicProject,
    CreatePrivateProject,
    EditProjectDetails,
    ProjectAccessibility
)
from functional_tests.selenium_tests.tests.projects.project_draw_on_map import (
    AddProjectWithExtent,
)
from functional_tests.selenium_tests.tests.projects.search_project import (
    ProjectSearch
)
from functional_tests.selenium_tests.tests.projects.project_resources import (
    AddResource
)
from functional_tests.selenium_tests.tests.projects.project_location import (
    AddLocation,
    EditLocation
)
from functional_tests.selenium_tests.tests.projects.location_resources import (
    AddLocationResource
)
from functional_tests.selenium_tests.tests.projects.location_relationships import (
    AddLocationRelationship
)
from functional_tests.selenium_tests.tests.projects.project_parties import (
    ViewParty,
    PartyResource,
    EditParty,
    DeleteParty
)
