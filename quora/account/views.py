from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny,IsAuthenticated

class UserRegistrationAPIView(APIView):
    def post(self , request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Both username and password are required'} ,
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'} ,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(username=username , password=password)

        refresh = RefreshToken.for_user(user)
        return Response({
            'user_id': user.id ,
            'username': user.username ,
            'access': str(refresh.access_token) ,
            'refresh': str(refresh)
        } , status=status.HTTP_201_CREATED)


class UserLoginAPIView(APIView):
    def post(self , request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username , password=password)

        if user is None:
            return Response(
                {'error': 'Invalid credentials'} ,
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            'user_id': user.id ,
            'username': user.username ,
            'access': str(refresh.access_token) ,
            'refresh': str(refresh)
        })


class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)