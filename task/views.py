from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from task.models import Task, SubTask
from task.permissions import CustomReadOnly
from task.serializers import SubTaskSerializer, TaskSerializer


class TasksAPI(APIView):
    permission_classes = [CustomReadOnly]
    
    def get(self, request):
        """전체 Task 목록 조회"""
        tasks = Task.objects.all()
        sub_tasks = SubTask.objects.all()  # 사용자가 속한 팀에 따라 결과 달라야 함
        serializer1 = TaskSerializer(tasks, many=True)
        serializer2 = SubTaskSerializer(sub_tasks, many=True)
        data = {
            'tasks': serializer1.data,
            'subTasks': serializer2.data
        }
        return Response(data, status=status.HTTP_200_OK)


class TaskAPI(APIView):
    permission_classes = [CustomReadOnly]
    
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
