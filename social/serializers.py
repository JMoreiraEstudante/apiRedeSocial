from rest_framework import serializers
from .models import Comment, Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'likes', 'created_date', 'last_modified')

class PostFollowingSerializer(serializers.ModelSerializer):
    comments= serializers.IntegerField()
    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'likes', 'comments', 'created_date', 'last_modified')

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id',"post", 'author', 'content', 'likes', 'created_date', 'last_modified')
