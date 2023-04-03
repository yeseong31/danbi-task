from rest_framework import generics, status
from rest_framework.response import Response

from account.models import User
from account.serializers import RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        # Serializer 통과 후 얻어온 토큰을 그대로 응답해 주는 방식
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data
        return Response({'token': token.key}, status=status.HTTP_200_OK)
