from django.urls import path

from task.views import TasksAPI

app_name = 'task'

urlpatterns = [
    path('', TasksAPI.as_view()),
]