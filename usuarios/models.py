# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User  

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200, blank=False)
    date_create = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=40)
    likes = models.ManyToManyField(User, related_name='post_like')


    class Meta:
        ordering = ['-date_create']
    
    @property
    def view_count(self):
        return Like.objects.filter(post=self).count()

    @property
    def cantidad_comentarios(self):
        return Comment.objects.filter(post=self).count()

    @property
    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=200, blank=False)
    date_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user) + ', ' + self.post.content[:40]


