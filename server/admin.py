from django.contrib import admin
from server.models import UserInfo, CourseInfo, OrderInfo

# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')

class CourseInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_name', 'teacher_name')

class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'course_id', 'teacher_name', 'student_name')

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(CourseInfo, CourseInfoAdmin)
admin.site.register(OrderInfo, OrderInfoAdmin)