from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name=('user'))
    QQnumber=models.CharField(max_length=20)
    PayUser=models.CharField(max_length=20)
    PayPSW=models.CharField(max_length=20)

    def __str__(self):
        return self.username

admin.site.register(UserInfo)
