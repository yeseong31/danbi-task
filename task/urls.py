from django.urls import path

from task.views.sub_task_views import sub_task_update
from task.views.task_views import task_list, task_detail, task_create, task_update

app_name = 'task'

urlpatterns = [
    path('', task_list, name='task_list'),
    path('detail/<int:pk>/', task_detail, name='task_detail'),
    path('create/', task_create, name='task_create'),
    path('update/<int:pk>/', task_update, name='task_update'),
    path('update/sub/<int:pk>/', sub_task_update, name='sub_task_update'),
]
