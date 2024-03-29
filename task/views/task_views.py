import os
from datetime import datetime

import jwt
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.models import User, Team
from config.settings import SECRET_KEY
from task.models import Task, SubTask
from task.permissions import CustomReadOnly
from task.serializers import TaskDetailSerializer, SubTaskDetailSerializer, TaskListSerializer, TaskCreateSerializer, \
    SubTaskCreateSerializer, TaskUpdateSerializer


class TasksView(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        Task 목록 조회
        """
        try:
            tasks = Task.objects.all()
            access = request.headers.get('Authorization')
            if access is not None:
                payload = jwt.decode(access.split()[-1], SECRET_KEY, algorithms=['HS256'])
                user = get_object_or_404(User, pk=payload.get('user_id'))
                team = get_object_or_404(Team, pk=user.team.id)
                sub_tasks = SubTask.objects.filter(team=team)
                data = {
                    'task': TaskListSerializer(tasks, many=True).data,
                    'sub_task': SubTaskDetailSerializer(sub_tasks, many=True).data
                }
            else:
                data = {
                    'task': TaskListSerializer(tasks, many=True).data
                }
            return Response(data, status=status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError:
            return Response({'message': '로그인 세션이 만료되었습니다. 다시 로그인해주세요.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.InvalidTokenError:
            return Response({'message': '토큰이 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        """
        Task 생성

        :args:
        - title: Task 이름
        - content: Task 설명
        - team_list: 하위 업무로 지정할 팀 ID 리스트
        """
        try:
            access = request.headers.get('Authorization')
            if access is None:
                raise jwt.exceptions.ExpiredSignatureError
            payload = jwt.decode(access.split()[-1], os.getenv('SECRET_KEY'), algorithms=['HS256'])
            user = get_object_or_404(User, pk=payload.get('user_id'))

            title = request.data.get('title')
            content = request.data.get('content')
            team_list = request.data.get('team_list')

            if not (title and content and (team_list or len(team_list) == 0)):
                return Response({'message': '필요한 정보가 모두 주어지지 않았습니다.'},
                                status=status.HTTP_400_BAD_REQUEST)

            team_list = [get_object_or_404(Team, pk=i) for i in team_list]

            task = Task.objects.create(
                create_user=user,
                title=title,
                content=content,
                team=user.team
            )
            task.save()

            sub_task_list = []
            for team in team_list:
                sub_task = SubTask.objects.create(
                    team=team,
                    task=task
                )
                sub_task.save()
                sub_task_list.append(SubTaskCreateSerializer(sub_task).data)

            response = TaskCreateSerializer(task).data
            response['sub_task'] = sub_task_list
            return Response(response, status=status.HTTP_201_CREATED)

        except jwt.exceptions.ExpiredSignatureError:
            return Response({'message': '로그인 세션이 만료되었습니다. 다시 로그인해주세요.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.InvalidTokenError:
            return Response({'message': '토큰이 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


class TaskView(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def get(self, request, pk):
        """
        Task 상세 조회

        :params:
        - pk: Task ID
        """
        task = get_object_or_404(Task, pk=pk)
        data = TaskDetailSerializer(task).data
        data['sub_task'] = [SubTaskDetailSerializer(s).data for s in task.subtask_set.all()]
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
        Task 수정

        :params:
        - pk: Task ID

        :args:
        - title: Task 이름
        - content: Task 설명
        - team_list: 하위 업무로 지정할 팀 ID 리스트
        """
        try:
            access = request.headers.get('Authorization')
            if access is None:
                raise jwt.exceptions.ExpiredSignatureError
            payload = jwt.decode(access.split()[-1], SECRET_KEY, algorithms=['HS256'])
            user = get_object_or_404(User, pk=payload.get('user_id'))

            task = get_object_or_404(Task, pk=pk)
            if user.id != task.create_user.id:
                return Response({'message': 'Task 작성자만 수정할 수 있습니다.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            title = request.data.get('title')
            content = request.data.get('content')
            team_list = request.data.get('team_list')  # 새롭게 하위 업무를 담당할 팀 ID 리스트

            if not (title and content and team_list):
                return Response({'message': '필요한 정보가 모두 주어지지 않았습니다.'},
                                status=status.HTTP_400_BAD_REQUEST)

            task.title = title
            task.content = content

            check = set()
            sub_task_list = task.subtask_set.all()
            for i, s in enumerate(sub_task_list):
                if s.team.pk not in team_list:
                    target_sub_task = sub_task_list[i]
                    if target_sub_task.is_complete:
                        return Response({'message': '이미 완료된 하위 업무는 삭제할 수 없습니다.'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    target_sub_task.delete()
                else:
                    check.add(s.team.pk)

            for i in team_list:
                if i not in check:
                    sub_task = SubTask.objects.create(
                        team=get_object_or_404(Team, pk=i),
                        task=task
                    )
                    sub_task.save()

            task.modified_at = datetime.now()
            task.save()

            data = TaskUpdateSerializer(task).data
            data['sub_task'] = [SubTaskDetailSerializer(s).data for s in task.subtask_set.all()]
            return Response(data, status=status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError:
            return Response({'message': '로그인 세션이 만료되었습니다. 다시 로그인해주세요.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.InvalidTokenError:
            return Response({'message': '토큰이 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
