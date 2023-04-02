from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase

from account.models import User, Team


class TeamModelTest(TestCase):
    def test_default_values(self):
        team = Team.objects.create(
            name='테스트팀'
        )
        self.assertEqual(team.name, '테스트팀')


class UserModelTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.register_url = '/auth/signup/'
        self.login_url = '/auth/login/'
        self.team = Team.objects.create(
            name='테스트팀'
        )
        self.user = User.objects.create_user(
            email='user1@test.com',
            username='user1',
            team=self.team,
            pw='!test@1234?',
        )

    def test_default_values(self):
        self.assertEqual(self.user.email, 'user1@test.com')
        self.assertEqual(self.user.username, 'user1')
        self.assertEqual(self.user.team, self.team)
        self.assertEqual(self.user.check_password('!test@1234?'), True)
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_admin, False)
