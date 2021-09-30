from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer, UpdateUserSerializer, UpdateFollowing
from .models import NewUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from django.http.response import Http404
from django.shortcuts import get_object_or_404

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

@api_view(['POST'])
def followed(request, **kwargs):
    try:
        follower = get_object_or_404(NewUser, pk=kwargs['pk'])
        serializer = UpdateFollowing(follower, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Http404:
        return Response("Seguidor com esse id não existe", status=status.HTTP_404_NOT_FOUND)

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