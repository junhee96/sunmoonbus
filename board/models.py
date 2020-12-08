# 2015244044 이준희
# 블로그,댓글,문의하기 데이터베이스
from django.db import models
from accounts.models import *
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to="images/post",blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.author

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.author

class SecretBorad(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    image=models.ImageField(upload_to="images/secret",blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    private = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class SecretComment(models.Model):
    secretborad = models.ForeignKey('SecretBorad', on_delete=models.CASCADE,related_name='SecretComment')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    class Meta:
        ordering = ['-created_at']
