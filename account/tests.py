from django.test import TestCase

from account.models import User


class UserModelTest(TestCase):
    def test_default_values(self):
        user = User.objects.create(email='test@test.com',
                                   username='test_nickname_1',
                                   team=None,
                                   password='!test@1234?')
        self.assertEqual(user.email, 'test@test.com')
        self.assertEqual(user.username, 'test_nickname_1')
        self.assertEqual(user.password, '!test@1234?')
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_admin, False)

