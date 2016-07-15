from django.db import models
from django.contrib import admin
import datetime
import django.utils.timezone as timezone

# Create your models here.

class UserInfo(models.Model):
    #userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    QQnumber=models.CharField(max_length=20)
    PayUser=models.CharField(max_length=20)
    PayPSW=models.CharField(max_length=20)
    info=models.CharField(max_length=200, default='勤奋刻苦，品学兼优，力争上游')
    time=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "ID:"+str(self.id)+", Name: "+self.username

class ConnectUser(models.Model):
    uuid = models.CharField(max_length=150, primary_key=True)
    username = models.CharField(max_length=20)

class CourseInfo(models.Model):
    course_name = models.CharField(max_length=50)
    teacher_id = models.BigIntegerField()
    teacher_name = models.CharField(max_length=20) #这列为了方便按教师搜索课程
    course_info = models.TextField(max_length=500)
    jwb_credit = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    time=models.DateTimeField(default=timezone.now)

class OrderInfo(models.Model):
    course_id = models.BigIntegerField()
    teacher_id = models.BigIntegerField()
    student_id = models.BigIntegerField()
    course_name = models.CharField(max_length=50)
    teacher_name = models.CharField(max_length=50)
    student_name = models.CharField(max_length=50)
    order_info = models.CharField(max_length=200)
    order_state = models.CharField(max_length=50)
    time=models.DateTimeField(default=timezone.now)

class AppVeri(models.Model):
    app_key = models.CharField(max_length=50)



admin.site.register(ConnectUser)
admin.site.register(UserInfo)
admin.site.register(CourseInfo)
admin.site.register(OrderInfo)
admin.site.register(AppVeri)


