from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User, Team
from task.models import Task


class TestTask(APITestCase):
    def setUp(self) -> None:
        self.team1 = Team.objects.create(name='테스트팀1')  # 1번 팀
        self.team2 = Team.objects.create(name='테스트팀2')  # 2번 팀
        self.team3 = Team.objects.create(name='테스트팀3')  # 3번 팀

        # 테스트 사용자
        self.email = 'kim@test.com'
        self.username = 'kim'
        self.pw = '!Test123?'
        self.user = User.objects.create_user(
            email=self.email,
            username=self.username,
            team=self.team1,
        )
        self.user.set_password(self.pw)
        self.user.save()

        # 테스트 Task
        self.task1 = Task.objects.create(
            create_user=self.user,
            team=self.team1,
            title='테스트 업무 1번',
            content='테스트 업무 1번에 대한 설명입니다.'
        )
        self.task2 = Task.objects.create(
            create_user=self.user,
            team=self.team1,
            title='테스트 업무 2번',
            content='테스트 업무 2번에 대한 설명입니다.'
        )

        # URL
        self.login_url = '/api/accounts/v1/login/'
        self.task_url = '/task/'

        # Bearer Token
        self.token = self.client.post(
            self.login_url,
            data={'email': self.email, 'pw': self.pw},
            format='json'
        ).data['token']['access']
    
    def test_create_task(self):
        # 새롭게 생성할 Task
        data = {
            'title': '테스트 업무',
            'content': '테스트 업무 설명입니다.',
            'team_list': [1, 2, 3]  # 하위업무로 등록할 팀 ID 리스트
        }
        response = self.client.post(
            path=self.task_url,
            data=data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        )
        result = response.data
        # print(result)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result['team']['id'], self.team1.id)
        self.assertEqual(result['title'], '테스트 업무')
        self.assertEqual(result['content'], '테스트 업무 설명입니다.')
        self.assertEqual(result['create_user']['username'], self.username)
        self.assertEqual(result['create_user']['team'], self.team1.id)
        self.assertEqual(result['sub_task'][0]['team']['id'], self.team1.id)
        self.assertEqual(result['sub_task'][1]['team']['id'], self.team2.id)
        self.assertEqual(result['sub_task'][2]['team']['id'], self.team3.id)
        
    def test_create_task_without_login(self):
        data = {
            'title': '테스트 업무',
            'content': '테스트 업무 설명입니다.',
            'team_list': [1, 2, 3]
        }
        response = self.client.post(
            path=self.task_url,
            data=data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_task(self):
        response = self.client.get(path=f'{self.task_url}{self.task1.id}/')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_non_existent_task(self):
        response = self.client.get(path='/task/12345/')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_get_task_list(self):
        response = self.client.get(path=self.task_url)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['task']), 2)
