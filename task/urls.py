from django.urls import path

from task.views.sub_task_views import SubTaskView
from task.views.task_views import TasksView, TaskView

app_name = 'task'

urlpatterns = [
    path('', TasksView.as_view(), name='TasksView'),
    path('<int:pk>/', TaskView.as_view(), name='TaskView'),
    path('sub/<int:pk>/', SubTaskView.as_view(), name='SubTaskView'),
]
