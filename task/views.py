from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from task.models import Task, SubTask
from task.permissions import CustomReadOnly
from task.serializers import TaskDetailSerializer, SubTaskSerializer, TaskListSerializer


class TasksAPI(APIView):
    permission_classes = [CustomReadOnly]
    
    def get(self, request):
        tasks = Task.objects.all()
        sub_tasks = SubTask.objects.all()  # 사용자가 속한 팀에 따라 결과 달라야 함
        data = {
            'task': TaskListSerializer(tasks, many=True).data,
            'subTask': SubTaskSerializer(sub_tasks, many=True).data
        }
        return Response(data, status=status.HTTP_200_OK)


class TaskAPI(APIView):
    permission_classes = [CustomReadOnly]
    
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        data = TaskDetailSerializer(task).data
        data['sub_task'] = [SubTaskSerializer(s).data for s in task.subtask_set.all()]
        return Response(data, status=status.HTTP_200_OK)
