from datetime import datetime

from django.db import models

from account.models import User, Team


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='작성자')
    team = models.ManyToManyField(Team, null=False, blank=False, verbose_name='업무 진행 팀', related_name='task_team')
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='업무명')
    content = models.TextField(null=True, blank=True, verbose_name='업무 내용')
    is_complete = models.BooleanField(default=False, verbose_name='업무 완료 여부')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='업무 완료일')
    created_at = models.DateTimeField(default=datetime.now(), null=False, blank=False, verbose_name='업무 생성일')
    modified_at = models.DateTimeField(null=True, blank=True, verbose_name='업무 수정일')

    def __str__(self):
        return f'[Task {self.id}] {self.title}'

    class Meta:
        db_table = 'task'


class SubTask(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ManyToManyField(Team, null=False, blank=False, verbose_name='하위업무 진행 팀', related_name='subtask_team')
    is_complete = models.BooleanField(default=False, verbose_name='하위업무 완료 여부')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='하위업무 완료일')
    created_at = models.DateTimeField(default=datetime.now(), null=False, blank=False, verbose_name='하위업무 생성일')
    modified_at = models.DateTimeField(null=True, blank=True, verbose_name='하위업무 수정일')

    def __str__(self):
        return f'[SubTask {self.id}]'

    class Meta:
        db_table = 'subtask'
