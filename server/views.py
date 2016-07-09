from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse

from django import forms
from server.models import UserInfo
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def userlogin(request):
    username = request.POST.get('username', '')
    password = request.POST.get('userpwd', '')
    user = authenticate(username=username, password=password)
    #user = authenticate(username = request.POST.get['username'], password=request.POST['password'])
    if user is not None:
        login(request, user)
        return HttpResponse('loginsuccess')
    else:
        return HttpResponse('loginfail')

def userlogout(request):
    logout(request)
    return HttpResponse('logout')

def check(request):
    if request.user.is_authenticated():
        user = request.user;
        return HttpResponse('login')
    else:
        return HttpResponse('fail')


class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())



def UserRegister(request):
    if request.user.is_authenticated():#已经登录
        return HttpResponse('alreadylogin')

    if request.method=='POST':
        username=request.POST.get('name','')
        password1=request.POST.get('password','')
        password2=request.POST.get('passwordrepeat')
        email=request.POST.get('email','')
        errors=[]

    if password1 != password2:
        errors.append('password not consistent')
        return HttpResponse(errors)

    filterResult=User.objects.filter(username=username)
    if len(filterResult)>0:
        errors.append('user already exist')
        return HttpResponse(errors)

    user=User()
    user.username=username
    user.set_password(password1)
    user.email=email
    user.save()

    newUser = authenticate(username=username, password=password1)  #注册后自动登录
    if newUser is not None:
        login(request, newUser)
        return HttpResponse('regisSuccess')










