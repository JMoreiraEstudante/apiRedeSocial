from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from user.models import NewUser
from django.db.models import Count
from .serializers import PostSerializer, UpdatePostSerializer, CommentSerializer, UpdateCommentSerializer, PostFollowingSerializer
from rest_framework.decorators import api_view
from django.db.models import Q

'''class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user'''

class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostFollowing(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostFollowingSerializer

    def get_queryset(self):
        user = NewUser.objects.filter(id=self.kwargs['pk']).first()
        posts = Post.objects.filter(Q(author__in = user.following.all()) | Q(author = user.id)).order_by('-created_date').annotate(comments=Count('comment'))
        return posts

class CommentList(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['pk'])

class PostDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class PostUser(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.kwargs['pk'])

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

@api_view(['POST'])
def commentLiked(request, **kwargs):
    try:
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        serializer = UpdateCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Http404:
        return Response("Comment com esse id não existe", status=status.HTTP_404_NOT_FOUND)
