from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from account.models import User, Team


class UserRegisterViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.register_url = '/api/accounts/v1/signup/'
        self.login_url = '/api/accounts/v1/login/'
        
        self.team = Team.objects.create(name='테스트팀')  # 1번 팀
        
        self.email = 'kim@test.com'
        self.username = 'kim'
        self.pw = '!Test123?'
        self.user = User.objects.create_user(
            email=self.email,
            username=self.username,
            team=self.team
        )
        self.user.set_password(self.pw)
        self.user.save()
    
    def test_default_values(self):
        self.assertEqual(self.user.email, 'kim@test.com')
        self.assertEqual(self.user.username, 'kim')
        self.assertEqual(self.user.team, self.team)
        self.assertEqual(self.user.check_password('!Test123?'), True)
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_admin, False)
        self.assertEqual(self.register_url, '/api/accounts/v1/signup/')
        self.assertEqual(self.login_url, '/api/accounts/v1/login/')
    
    def test_register(self):
        email = 'han@test.com'
        username = 'han'
        team = self.team.id
        pw = '!Test1234?'
        
        data = {
            'email': email,
            'username': username,
            "team": team,
            'pw': pw
        }
        
        response = self.client.post(
            self.register_url,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['email'], email)
        self.assertEqual(response.data['user']['username'], username)
        self.assertEqual(response.data['user']['team'], team)
        
    def test_login(self):
        email = 'kim@test.com'
        pw = '!Test123?'
        self.assertEqual(self.email, email)
        self.assertEqual(self.pw, pw)
        
        response = self.client.post(
            self.login_url,
            data={'email': email, 'pw': pw},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['email'], email)
