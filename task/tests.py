from django.shortcuts import get_object_or_404
from rest_framework.test import APIRequestFactory, APITestCase

from account.models import User, Team
from task.models import Task


class TestTask(APITestCase):
    def setUp(self) -> None:
        self.team = Team.objects.create(name='test_team')
        self.user = User.objects.create(
            email='testname@test.com',
            username='test_name',
            team=self.team
        )
        self.user.set_password('!Test123?')
        self.task = Task.objects.create(
            create_user=self.user,
            team=self.team,
            title='테스트업무1',
            content='테스트 업무입니다.'
        )
        self.user.save()
    
    def test_create_task(self):
        test_task = Task.objects.create(
            create_user=self.user,
            team=self.team,
            title='테스트업무1',
            content='테스트 업무입니다.'
        )
        self.assertEqual(test_task.create_user, self.user)
        self.assertEqual(test_task.team, self.team)
        self.assertEqual(test_task.title, '테스트업무1')
        self.assertEqual(test_task.content, '테스트 업무입니다.')
        self.assertEqual(len(Task.objects.all()), 2)
    
    def test_get_task(self):
        test_task = get_object_or_404(Task, id=self.task.id)
        self.assertEqual(test_task.create_user, self.task.create_user)
        self.assertEqual(test_task.team, self.task.team)
        self.assertEqual(test_task.title, self.task.title)
        self.assertEqual(test_task.content, self.task.content)
    
    def test_update_task(self):
        title = '테스트업무2'
        content = '테스트 업무 두 번째입니다.'
        test_task = get_object_or_404(Task, id=self.task.id)
        test_task.title = title
        test_task.content = content
        self.assertEqual(test_task.title, '테스트업무2')
        self.assertEqual(test_task.content, '테스트 업무 두 번째입니다.')
    
    def test_delete_task(self):
        self.task.delete()
        self.assertEqual(len(Task.objects.all()), 0)
