import os

import jwt
from rest_framework import status
from rest_framework.decorators import authentication_classes, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.models import User, Team
from task.models import Task, SubTask
from task.permissions import CustomReadOnly
from task.serializers import TaskDetailSerializer, SubTaskDetailSerializer, TaskListSerializer, TaskCreateSerializer, \
    SubTaskCreateSerializer, TaskUpdateSerializer


@api_view(['GET'])
@permission_classes([CustomReadOnly])
@authentication_classes([JWTAuthentication])
def task_list(request):
    # 사용자가 로그인을 한 경우에만 사용자의 팀을 찾을 수 있음...!!
    # print(request.COOKIES['access'])
    tasks = Task.objects.all()
    sub_tasks = SubTask.objects.all()  # 사용자가 속한 팀에 따라 결과 달라야 함
    data = {
        'task': TaskListSerializer(tasks, many=True).data,
        'subTask': SubTaskDetailSerializer(sub_tasks, many=True).data
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([CustomReadOnly])
@authentication_classes([JWTAuthentication])
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    data = TaskDetailSerializer(task).data
    data['sub_task'] = [SubTaskDetailSerializer(s).data for s in task.subtask_set.all()]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([CustomReadOnly])
@authentication_classes([JWTAuthentication])
def task_create(request):
    """
    Task 생성
    
    :params:
    - title: Task 이릅
    - content: Task 내용
    - team: 하위 업무로 지정한 팀(ID) 리스트
    """
    try:
        access = request.headers.get('Authorization').split()[1]
        payload = jwt.decode(access, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        user = get_object_or_404(User, pk=payload.get('user_id'))
        
        title = request.data.get('title')
        content = request.data.get('content')
        team = request.data.get('team')
        
        if not (title and content and team):
            return Response({'message': '필요한 정보가 모두 주어지지 않았습니다.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        team_list = [get_object_or_404(Team, pk=i) for i in team]
        
        task = Task.objects.create(
            create_user=user,
            title=title,
            content=content,
        )
        for team in team_list:
            task.team.add(team)
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
        return Response(response, status=status.HTTP_200_OK)
    
    except jwt.exceptions.ExpiredSignatureError:
        return Response({'message': '로그인 세션이 만료되었습니다. 다시 로그인해주세요.'},
                        status=status.HTTP_401_UNAUTHORIZED)
    
    except jwt.exceptions.InvalidTokenError:
        return Response({'message': '토큰이 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PUT'])
@permission_classes([CustomReadOnly])
@authentication_classes([JWTAuthentication])
def task_update(request, pk):
    """
    Task 수정

    :params:
    - title: Task 이릅
    - content: Task 내용
    - team: 하위 업무로 지정한 팀(ID) 리스트
    """
    try:
        access = request.headers.get('Authorization').split()[1]
        payload = jwt.decode(access, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        user = get_object_or_404(User, pk=payload.get('user_id'))
        
        task = get_object_or_404(Task, pk=pk)
        if user.id != task.create_user.id:
            return Response({'message': 'Task 작성자만 수정할 수 있습니다.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        title = request.data.get('title')
        content = request.data.get('content')
        new_team_pk_list = request.data.get('team')
        
        if not (title and content and new_team_pk_list):
            return Response({'message': '필요한 정보가 모두 주어지지 않았습니다.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        task.title = title
        task.content = content
        old_team_pk_list = [s.team.id for s in task.subtask_set.all()]
        
        # SubTask 삭제 가능 여부 확인
        check = [0] * 8
        for i in range(1, 8):
            if i in new_team_pk_list:
                check[i] += 1
            if i in old_team_pk_list:
                check[i] -= 1
            if check[i] == -1:  # 삭제
                target_sub_task = task.subtask_set.get(team=get_object_or_404(Team, pk=i))
                if target_sub_task.is_complete:
                    return Response({'message': '이미 완료된 하위 업무는 삭제할 수 없습니다.'},
                                    status=status.HTTP_400_BAD_REQUEST)
                target_sub_task.delete()

        # 새로운 SubTask 생성
        for i in range(1, 8):
            team = get_object_or_404(Team, pk=i)
            if i not in new_team_pk_list:
                task.team.remove(team)
            else:
                task.team.add(team)
            if check[i] == 1:
                SubTask.objects.create(
                    team=team,
                    task=task
                ).save()
        task.save()
        
        response = TaskUpdateSerializer(task).data
        return Response(response, status=status.HTTP_200_OK)
    
    except jwt.exceptions.ExpiredSignatureError:
        return Response({'message': '로그인 세션이 만료되었습니다. 다시 로그인해주세요.'},
                        status=status.HTTP_401_UNAUTHORIZED)
    
    except jwt.exceptions.InvalidTokenError:
        return Response({'message': '토큰이 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
