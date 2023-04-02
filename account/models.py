from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=False, blank=False, unique=True, verbose_name='팀 이름')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'team'


class UserManager(BaseUserManager):
    def create_user(self, email, username, team, pw=None, **extra_fields):
        if email is None:
            raise TypeError('이메일은 필수 입력 사항입니다.')
        if username is None:
            raise TypeError('이름은 필수 입력 사항입니다.')
        if pw is None:
            raise TypeError('비밀번호는 필수 입력 사항입니다.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            team=team,
            **extra_fields
        )
        user.set_password(pw)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, team, pw):
        user = self.create_user(
            email=email,
            username=username,
            team=team,
            password=pw
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=320, null=False, blank=False, unique=True, verbose_name='이메일')
    password = models.CharField(max_length=128, db_column='pw', verbose_name='비밀번호')
    username = models.CharField(max_length=128, null=False, blank=False, verbose_name='사용자 이름')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, verbose_name='소속된 팀')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'team', 'password']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    class Meta:
        db_table = 'user'
