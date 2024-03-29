from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from rest_framework.generics import get_object_or_404


class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, null=False, blank=False, unique=True, verbose_name='팀 이름')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'team'


class UserManager(BaseUserManager):
    def create_user(self, email, username, team, pw=None):
        if email is None:
            raise TypeError('이메일은 필수 입력 사항입니다.')
        if username is None:
            raise TypeError('이름은 필수 입력 사항입니다.')
        if team is None:
            raise TypeError('팀은 필수 입력 사항입니다.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            team=team
        )
        user.set_password(pw)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, team, password):
        team = get_object_or_404(Team, pk=team)
        user = self.create_user(
            email=email,
            username=username,
            team=team,
            pw=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True, verbose_name='이메일')
    username = models.CharField(max_length=128, null=False, blank=False, verbose_name='사용자 이름')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True, verbose_name='소속 팀')
    password = models.CharField(max_length=255, db_column='pw', verbose_name='비밀번호')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'team']

    def __str__(self):
        return self.username

    @property
    def is_superuser(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    class Meta:
        db_table = 'user'
