from accounts.models import User
from organization.models import Organization, Project
from party.models import Party

class DeleteTestData():

    def delete_test_users(self):
        users = User.objects.filter(username__startswith='test')
        for user in users:
            user.delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all test users.'))

    def delete_test_organizations(self):
        orgs = Organization.objects.filter(name__startswith='test')
        for org in orgs:
            org.delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all test organizations.'))

    def delete_test_projects(self):
        projects = Project.objects.filter(name__startswith='test')
        for project in projects:
            project.delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all test projects.'))
