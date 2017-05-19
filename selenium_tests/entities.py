class Credentials:

    test_username = "cadasta-test-user-1"
    test_password = "XYZ#qwerty"
    test_email = "cadasta-test-user-1@example.com"

    @staticmethod
    def get_test_username():
        return Credentials.test_username

    @staticmethod
    def set_test_username(username):
        Credentials.test_username = username

    @staticmethod
    def get_test_password():
        return Credentials.test_password

    @staticmethod
    def set_test_password(password):
        Credentials.test_password = password

    @staticmethod
    def get_test_email():
        return Credentials.test_email

    @staticmethod
    def set_test_email(email):
        Credentials.test_email = email


class Organization:

    test_org_name = "organization-1"

    @staticmethod
    def get_test_org_name():
        return Organization.test_org_name

    @staticmethod
    def set_test_org_name(org_name):
        Organization.test_org_name = org_name


class Project:

    test_proj_name = "project-1"

    @staticmethod
    def get_test_proj_name():
        return Project.test_proj_name

    @staticmethod
    def set_test_proj_name(proj_name):
        Project.test_proj_name = proj_name
