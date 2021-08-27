# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from usuarios.models import Post, Comment

# Register your models here.

admin.site.register(Post)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')
    list_filter = ('date_create',)
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


