from django.db import models
from django.conf import settings

class Post(models.Model):
    content = models.TextField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_date']