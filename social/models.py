from django.db import models
from django.conf import settings

class Post(models.Model):
    content = models.TextField(max_length=255)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_date']

class Comment(models.Model):
    content = models.TextField(max_length=255)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='comment_likes')
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post =  models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_date']