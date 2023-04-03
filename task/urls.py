from django.urls import path

from task.views import TasksAPI, TaskAPI

app_name = 'task'

urlpatterns = [
    path('', TasksAPI.as_view(), name='task_list'),
    path('<int:pk>/', TaskAPI.as_view(), name='task_detail'),
]
