from datetime import datetime

from django.db import models

from account.models import User, Team


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, verbose_name='create_user')
    team = models.ManyToManyField(Team, null=False, blank=False, verbose_name='team', related_name='task_team')
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='title')
    content = models.TextField(null=True, blank=True, verbose_name='content')
    is_complete = models.BooleanField(default=False, verbose_name='is_complete')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='completed_date')
    created_at = models.DateTimeField(default=datetime.now(), null=False, blank=False, verbose_name='created_at')
    modified_at = models.DateTimeField(null=True, blank=True, verbose_name='modified_at')

    def __str__(self):
        return f'[Task {self.id}] {self.title}'

    class Meta:
        db_table = 'task'


class SubTask(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=False, blank=False, verbose_name='team')
    is_complete = models.BooleanField(default=False, verbose_name='is_complete')
    completed_date = models.DateTimeField(null=True, blank=True, verbose_name='completed_date')
    created_at = models.DateTimeField(default=datetime.now(), null=False, blank=False, verbose_name='created_at')
    modified_at = models.DateTimeField(null=True, blank=True, verbose_name='modified_at')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=False, blank=False, verbose_name='task')

    def __str__(self):
        return f'[SubTask {self.id}]'

    class Meta:
        db_table = 'subtask'
