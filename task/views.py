from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from task.models import Task, SubTask
from task.serializers import SubTaskSerializer, TaskSerializer


class TasksAPI(APIView):
    def get(self, request):
        """전체 Task 정보 조회"""
        tasks = Task.objects.all()
        sub_tasks = SubTask.objects.all()  # 사용자가 속한 팀에 따라 결과 달라야 함
        serializer1 = TaskSerializer(tasks, many=True)
        serializer2 = SubTaskSerializer(sub_tasks, many=True)
        data = sorted(serializer1.data + serializer2.data, key=lambda x: x['created_at'])
        return Response(data, status=status.HTTP_200_OK)
