# 2015244044 이준희
# 사용자 DB 
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name


class EmailConfirm(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=30)
    is_confirmed = models.BooleanField(default=False)
    create_at = models.DateField(auto_now_add=True)
        