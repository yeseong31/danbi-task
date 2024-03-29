from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User, Team
from task.models import Task, SubTask


class TestTask(APITestCase):
    def setUp(self) -> None:
        # Team
        self.team1 = Team.objects.create(name='단비')
        self.team2 = Team.objects.create(name='다래')
        self.team3 = Team.objects.create(name='블라블라')
        self.team4 = Team.objects.create(name='철로')
        self.team5 = Team.objects.create(name='땅이')
        self.team6 = Team.objects.create(name='해태')
        self.team7 = Team.objects.create(name='수피')

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

        # 2번 Task의 하위 업무로 등록된 테스트 SubTask
        self.sub_task1 = SubTask.objects.create(team=self.team1, task=self.task2)
        self.sub_task2 = SubTask.objects.create(team=self.team2, task=self.task2, is_complete=True)
        self.sub_task3 = SubTask.objects.create(team=self.team3, task=self.task2, is_complete=True)

        # URL
        self.login_url = '/api/accounts/v1/login/'
        self.task_url = '/task/'
        self.sub_task_url = '/task/sub/'

        # Bearer Token(로그인 토큰)
        self.token = self.client.post(
            self.login_url,
            data={'email': 'kim@test.com', 'pw': '!Test123?'},  # self.user1 로그인
            format='json'
        ).data['token']['access']

    def test_create_task(self):
        """
        Task 생성 테스트
        """
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
        """
        Task 생성 테스트 - SubTask로 지정할 팀을 전달하지 않은 경우
        """
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
        """
        Task 생성 테스트 - 로그인을 하지 않은 경우
        """
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
        """
        Task 상세 조회
        """
        response = self.client.get(path=f'{self.task_url}{self.task1.id}/')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existent_task(self):
        """
        Task 상세 조회 - 존재하지 않는 Task인 경우
        """
        response = self.client.get(path='/task/12345/')
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_task_list(self):
        """
        Task 목록 조회
        """
        response = self.client.get(
            path=self.task_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['task']), 2)
        self.assertEqual(len(response.data['sub_task']), 1)

    def test_update_task(self):
        """
        Task 수정 테스트
        """
        data = {
            'title': '수정된 테스트 업무',
            'content': '수정된 테스트 업무 설명입니다.',
            'team_list': [self.team2.id, self.team3.id, self.team6.id]  # 1번 팀 삭제, 6번 팀 추가
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
        self.assertEqual(response.data['sub_task'][0]['team']['id'], self.team2.id)
        self.assertEqual(response.data['sub_task'][1]['team']['id'], self.team3.id)
        self.assertEqual(response.data['sub_task'][2]['team']['id'], self.team6.id)

    def test_update_task_without_login(self):
        """
        Task 수정 테스트 - 로그인을 하지 않은 경우
        """
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
        """
        Task 수정 테스트 - 완료된 SubTask를 삭제하는 경우
        """
        data = {
            'title': '수정된 테스트 업무',
            'content': '수정된 테스트 업무 설명입니다.',
            'team_list': [self.team1.id, self.team2.id]  # 완료 처리된 3번 SubTask 삭제 시도
        }
        response = self.client.put(
            path=f'{self.task_url}{self.task2.id}/',
            data=data,
            format='json',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task_for_non_author_user(self):
        """
        Task 수정 테스트 - 수정 권한이 없는 사용자인 경우
        """
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

    def test_handle_task_completion_when_all_sub_task_are_completed(self):
        """
        Task 완료 처리 테스트 - 모든 SubTask가 완료된 경우
        """
        response = self.client.put(
            path=f'{self.sub_task_url}{self.sub_task1.id}/',  # 아직 완료되지 않은 1번 SubTask 완료 처리
            **{'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.sub_task1.team.id, self.team1.id)  # 1번 SubTask는 담당 팀(1번)에서 완료 처리
        self.assertEqual(self.sub_task1.task.id, self.task2.id)  # 1번 SubTask는 2번 Task에 속함
        self.assertEqual(self.sub_task2.is_complete, True)  # 모든 SubTask 완료 처리 후 2번 Task 완료 처리

    def test_only_the_team_in_charge_corrects_the_sub_task(self):
        """
        Task 완료 처리 테스트 - SubTask에 소속되지 않은 팀인 경우
        """
        user2 = User.objects.create_user(
            email='han@test.com',
            username='han',
            team=self.team6,
        )
        user2.set_password('!Test456?')
        user2.save()

        token = self.client.post(
            self.login_url,
            data={'email': 'han@test.com', 'pw': '!Test456?'},  # self.user2 로그인
            format='json'
        ).data['token']['access']

        response = self.client.put(
            path=f'{self.sub_task_url}{self.sub_task2.id}/',  # 6번 팀에 속한 han이 다른 팀의 SubTask 완료 처리 시도
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_handle_sub_task_completion_that_have_already_been_completed(self):
        """
        SubTask 완료 처리 테스트 - 이미 완료 처리된 SubTask인 경우
        """
        user2 = User.objects.create_user(
            email='han@test.com',
            username='han',
            team=self.team2,  # 2번 팀
        )
        user2.set_password('!Test456?')
        user2.save()

        token = self.client.post(
            self.login_url,
            data={'email': 'han@test.com', 'pw': '!Test456?'},  # self.user2 로그인
            format='json'
        ).data['token']['access']
        
        response = self.client.put(
            path=f'{self.sub_task_url}{self.sub_task2.id}/',  # 이미 완료한 SubTask에 대해 완료 처리 시도
            **{'HTTP_AUTHORIZATION': f'Bearer {token}'}
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

