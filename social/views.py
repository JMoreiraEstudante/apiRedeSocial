from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer

'''class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user'''

class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostSerializer
    queryset = Post.objects.all()