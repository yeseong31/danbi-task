from django.urls import path

from task.views import task_list, task_detail, task_create, task_update

app_name = 'task'

urlpatterns = [
    path('', task_list, name='task_list'),
    path('detail/<int:pk>/', task_detail, name='task_detail'),
    path('create/', task_create, name='task_create'),
    path('update/<int:pk>/', task_update, name='task_update'),
]
