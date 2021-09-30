from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from user.models import NewUser
from .serializers import PostSerializer, UpdatePostSerializer
from rest_framework.decorators import api_view

'''class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user'''

class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

@api_view(['POST'])
def liked(request, **kwargs):
    try:
        post = get_object_or_404(Post, pk=kwargs['pk'])
        serializer = UpdatePostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Http404:
        return Response("Post com esse id não existe", status=status.HTTP_404_NOT_FOUND)
