from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'likes', 'created_date', 'last_modified')

class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('likes',)