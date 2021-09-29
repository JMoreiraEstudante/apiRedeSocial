from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, UpdateUserSerializer
from .models import NewUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions

class CustomUserCreate(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomUserSerializer
    queryset = NewUser.objects.all()

class UserUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UpdateUserSerializer
    queryset = NewUser.objects.all()

class UserList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = NewUser.objects.all()
    serializer_class = CustomUserSerializer

class BlacklistTokenUpdateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)