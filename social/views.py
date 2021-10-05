from django.http.response import Http404
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment, Notification
from user.models import NewUser
from django.db.models import Count
from .serializers import PostSerializer, CommentSerializer, PostFollowingSerializer, NotificationSerializer
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

    def create(self, request, *args, **kwargs):
        #default create
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.data)

        #notification
        sender = get_object_or_404(NewUser, pk=serializer.data['author'])
        post = get_object_or_404(Post, pk=serializer.data['post'])
        receiver = get_object_or_404(NewUser, pk=post.author.id)
        notification = Notification.objects.create(sender=sender, receiver=receiver, message="@{} comentou seu post!".format(sender.user_name))
        notification.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class NotificationAliveList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        #return Comment.objects.filter(post=self.kwargs['pk'])
        return Notification.objects.filter(receiver=self.kwargs['pk'], alive=True)

class NotificationAllList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.kwargs['pk']).order_by('-id')

class PostDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostFollowingSerializer
    queryset = Post.objects.all().annotate(comments=Count('comment'))

class PostUser(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PostFollowingSerializer

    def get_queryset(self):
        return Post.objects.filter(author=self.kwargs['pk']).annotate(comments=Count('comment'))

@api_view(['POST'])
def liked(request, **kwargs):
    try:
        post = get_object_or_404(Post, pk=kwargs['pk'])
        sender = get_object_or_404(NewUser, pk=request.data['like'])
        if (request.data['action'] == True):
            receiver = get_object_or_404(NewUser, pk=post.author.id)
            post.likes.add(sender)
            post.save()
            notification = Notification.objects.create(sender=sender, receiver=receiver, message="@{} curtiu seu post!".format(sender.user_name))
            notification.save()
            return Response("Adicionado o Like", status=status.HTTP_202_ACCEPTED)
        else:
            post.likes.remove(sender)
            post.save()
            return Response("Removido o Like", status=status.HTTP_202_ACCEPTED)
    except Http404:
        return Response("Esse id não existe", status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def commentLiked(request, **kwargs):
    try:
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        sender = get_object_or_404(NewUser, pk=request.data['like'])
        if (request.data['action'] == True):
            receiver = get_object_or_404(NewUser, comment.author)
            comment.likes.add(sender)
            comment.save()
            notification = Notification.objects.create(sender=sender, receiver=receiver, message="@{} curtiu seu comentário!".format(sender.user_name))
            notification.save()
            return Response("Adicionado o Like", status=status.HTTP_202_ACCEPTED)
        else:
            comment.likes.remove(sender)
            comment.save()
            return Response("Removido o Like", status=status.HTTP_202_ACCEPTED)
    except Http404:
        return Response("Eesse id não existe", status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def acknowledged(request, **kwargs):
    try:
        notification = get_object_or_404(Notification, pk=kwargs['pk'])
        notification.alive = False
        notification.save()
        return Response("Notificação reconhecida", status=status.HTTP_202_ACCEPTED)
    except Http404:
        return Response("Esse id não existe", status=status.HTTP_404_NOT_FOUND)
