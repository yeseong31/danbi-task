import os
from datetime import datetime

import jwt
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from account.models import User
from task.models import SubTask, Task
from task.permissions import CustomReadOnly
from task.serializers import SubTaskDetailSerializer


class SubTaskView(APIView):
    permission_classes = [CustomReadOnly]
    authentication_classes = [JWTAuthentication]

    def put(self, request, pk):
        """
        SubTask 수정

        :params:
        - pk: SubTask ID
        """
        try:
            access = request.headers.get('Authorization')

            if access is None:
                raise jwt.exceptions.ExpiredSignatureError
            payload = jwt.decode(access.split()[-1], os.getenv('SECRET_KEY'), algorithms=['HS256'])
            user = get_object_or_404(User, pk=payload.get('user_id'))
            sub_task = SubTask.objects.get(pk=pk)

            if user.team.id != sub_task.team.id:
                return Response({'message': '하위업무를 생성한 팀애 속한 사용자만이 완료 처리를 할 수 있습니다.'},
                                status=status.HTTP_401_UNAUTHORIZED)
            if sub_task.is_complete:
                return Response({'message': '이미 완료한 하위업무입니다.'},
                                status=status.HTTP_400_BAD_REQUEST)

            sub_task.is_complete = True
            end_time = datetime.now()
            sub_task.modified_at = end_time
            sub_task.completed_date = end_time
            sub_task.save()

            task = Task.objects.get(pk=sub_task.task.id)
            check = True
            for s in task.subtask_set.all():
                if not s.is_complete:
                    check = False
                    break
            if check:
                task.is_complete = True
                task.completed_date = end_time
                task.modified_at = end_time
                task.save()

            response = SubTaskDetailSerializer(sub_task).data
            return Response(response, status=status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError:
            return Response({'message': '로그인 세션이 만료되었습니다. 다시 로그인해주세요.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.InvalidTokenError:
            return Response({'message': '토큰이 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
