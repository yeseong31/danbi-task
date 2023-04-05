import os

import jwt
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from account.models import User
from account.serializers import RegisterSerializer, LoginSerializer


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token, access_token = str(token), str(token.access_token)
            response = Response(
                {
                    'user': serializer.data,
                    'message': 'SUCCESS: Register',
                    'token': {
                        'access': access_token,
                        'refresh': refresh_token
                    },
                },
                status=status.HTTP_201_CREATED
            )
            response.set_cookie('access', access_token, httponly=True)
            response.set_cookie('refresh', refresh_token, httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def get(self, request):
        try:
            access = request.COOKIES.get('access')
            payload = jwt.decode(access, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = LoginSerializer(instance=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except jwt.exceptions.ExpiredSignatureError:
            data = {
                'refresh': request.COOKIES.get('refresh', None)
            }
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access = serializer.data.get('access', None)
                refresh = serializer.data.get('refresh', None)
                payload = jwt.decode(access, os.getenv('SECRET_KEY'), algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_object_or_404(User, pk=pk)
                serializer = LoginSerializer(instance=user)
                response = Response(serializer.data, status=status.HTTP_200_OK)
                response.set_cookie('access', access)
                response.set_cookie('refresh', refresh)
                return response
            raise jwt.exceptions.InvalidTokenError

        except jwt.exceptions.InvalidTokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        email = request.data.get('email')
        pw = request.data.get('pw')
        user = get_object_or_404(User, email=email)
        if user is None or not user.check_password(pw):
            return Response({"message": "FAIL: Login"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = LoginSerializer(user)
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token, access_token = str(token), str(token.access_token)
        response = Response(
            {
                'user': serializer.data,
                'message': 'SUCCESS: Login',
                'token': {
                    'access': access_token,
                    'refresh': refresh_token
                },
            },
            status=status.HTTP_200_OK
        )
        response.set_cookie('access', access_token, httponly=True)
        response.set_cookie('refresh', refresh_token, httponly=True)
        return response

    def delete(self, request):
        response = Response({"message": "SUCCESS: Logout"}, status=status.HTTP_202_ACCEPTED)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response
