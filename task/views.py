from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from task.models import Task
from task.serializers import TaskSerializer


class TasksAPI(APIView):
    def get(self, request):
        """전체 Task 정보 조회"""
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """Task 정보 등록"""
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class TaskAPI(APIView):
    def get(self, request, tid):
        """하나의 Task 정보 조회"""
        task = get_object_or_404(Task, id=tid)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
