from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User, Team
from task.models import Task, SubTask


class TestTask(APITestCase):
    def setUp(self) -> None:
        self.team1 = Team.objects.create(name='단비')  # 1번 팀
        self.team2 = Team.objects.create(name='다래')  # 2번 팀
        self.team3 = Team.objects.create(name='블라블라')  # 3번 팀
        self.team4 = Team.objects.create(name='철로')  # 4번 팀
        self.team5 = Team.objects.create(name='땅이')  # 5번 팀
        self.team6 = Team.objects.create(name='해태')  # 6번 팀
        self.team7 = Team.objects.create(name='수피')  # 7번 팀
        
        # 테스트 사용자
        self.user1 = User.objects.create_user(
            email='kim@test.com',
            username='kim',
            team=self.team1,
        )
        self.user1.set_password('!Test123?')
        self.user1.save()
        
        # 테스트 Task
        self.task1 = Task.objects.create(
            create_user=self.user1,
            team=self.team1,
            title='테스트 업무 1번',
            content='테스트 업무 1번에 대한 설명입니다.'
        )
        self.task2 = Task.objects.create(
            create_user=self.user1,
            team=self.team1,
            title='테스트 업무 2번',
            content='테스트 업무 2번에 대한 설명입니다.'
        )
        
        # Task의 하위 업무로 등록된 테스트 SubTask
        self.sub_task1 = SubTask.objects.create(team=self.team1, task=self.task2, is_complete=True)
        self.sub_task2 = SubTask.objects.create(team=self.team2, task=self.task2, is_complete=True)
        self.sub_task3 = SubTask.objects.create(team=self.team3, task=self.task2)
        
        # URL
        self.login_url = '/api/accounts/v1/login/'
        self.task_url = '/task/'
        
        # Bearer Token
        self.token = self.client.post(
            self.login_url,
            data={'email': 'kim@test.com', 'pw': '!Test123?'},  # self.user1 로그인
            format='json'
        ).data['token']['access']
    
    def test_create_task(self):
        data = {
            'title': '테스트 업무',
            'content': '테스트 업무 설명입니다.',
            'team_list': [self.team1.id, self.team2.id, self.team3.id]  # 하위 업무로 등록할 팀 ID 리스트
        }
        response = self.client.post(
            path=self.task_url,
            data=data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['team']['id'], self.team1.id)
        self.assertEqual(response.data['title'], '테스트 업무')
        self.assertEqual(response.data['content'], '테스트 업무 설명입니다.')
        self.assertEqual(response.data['create_user']['username'], 'kim')
        self.assertEqual(response.data['create_user']['team'], self.team1.id)
        self.assertEqual(response.data['sub_task'][0]['team']['id'], self.team1.id)
        self.assertEqual(response.data['sub_task'][1]['team']['id'], self.team2.id)
        self.assertEqual(response.data['sub_task'][2]['team']['id'], self.team3.id)
    
    def create_task_without_filling_team_list(self):
        data = {
            'title': '테스트 업무',
            'content': '테스트 업무 설명입니다.',
            'team_list': []
        }
        response = self.client.post(
            path=self.task_url,
            data=data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_task_without_login(self):
        data = {
            'title': '테스트 업무',
            'content': '테스트 업무 설명입니다.',
            'team_list': [self.team1.id, self.team2.id, self.team3.id]
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
    
    def test_update_task(self):
        data = {
            'title': '수정된 테스트 업무',
            'content': '수정된 테스트 업무 설명입니다.',
            'team_list': [self.team1.id, self.team2.id, self.team6.id]  # 3번 팀 삭제, 6번 팀 추가
        }
        response = self.client.put(
            path=f'{self.task_url}{self.task2.id}/',
            data=data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['team']['id'], self.team1.id)
        self.assertEqual(response.data['title'], '수정된 테스트 업무')
        self.assertEqual(response.data['content'], '수정된 테스트 업무 설명입니다.')
        self.assertEqual(response.data['create_user']['username'], 'kim')
        self.assertEqual(response.data['create_user']['team'], self.team1.id)
        self.assertEqual(response.data['sub_task'][0]['team']['id'], self.team1.id)
        self.assertEqual(response.data['sub_task'][1]['team']['id'], self.team2.id)
        self.assertEqual(response.data['sub_task'][2]['team']['id'], self.team6.id)
    
    def test_update_task_without_login(self):
        data = {
            'title': '수정된 테스트 업무',
            'content': '수정된 테스트 업무 설명입니다.',
            'team_list': [self.team1.id, self.team6.id]
        }
        response = self.client.put(
            path=f'{self.task_url}{self.task2.id}/',
            data=data,
            format='json',
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_update_task_contains_completed_sub_tasks(self):
        self.sub_task1.is_complete = True
        self.sub_task1.save()
        
        data = {
            'title': '수정된 테스트 업무',
            'content': '수정된 테스트 업무 설명입니다.',
            'team_list': [self.team2.id, self.team3.id]  # 완료 처리된 1번 SubTask 삭제 시도
        }
        response = self.client.put(
            path=f'{self.task_url}{self.task2.id}/',
            data=data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        )
        # print(response.data)
        
        self.sub_task1.is_complete = False  # 다른 테스트를 위해 완료 처리 rollback
        self.sub_task1.save()
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_update_task_for_non_author_user(self):
        user2 = User.objects.create_user(
            email='han@test.com',
            username='han',
            team=self.team2,
        )
        user2.set_password('!Test456?')
        user2.save()
        
        token = self.client.post(
            self.login_url,
            data={'email': 'han@test.com', 'pw': '!Test456?'},  # self.user2 로그인
            format='json'
        ).data['token']['access']
        
        data = {
            'title': '수정된 테스트 업무',
            'content': '수정된 테스트 업무 설명입니다.',
            'team_list': [self.team1.id, self.team6.id]
        }
        response = self.client.put(
            path=f'{self.task_url}{self.task2.id}/',
            data=data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
