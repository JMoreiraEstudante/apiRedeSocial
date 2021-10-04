from django.contrib import admin
from . import models

@admin.register(models.Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('id', 'author')

@admin.register(models.Comment)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('id', 'post','author')

@admin.register(models.Notification)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('id','receiver','sender')