from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from django import forms
from server.models import UserInfo
from server.models import ConnectUser
from server.models import CourseInfo
from server.models import OrderInfo
from server.models import AppVeri
import uuid
import json
import time
import django.utils.timezone as timezone
from django.db.models import Q

# Create your views here.
#用户注册
def UserRegister(request):
    if request.method=='POST':
        username=request.POST.get('username','')
        password=request.POST.get('userpwd','')
        email=request.POST.get('email','')

    filterResult=UserInfo.objects.filter(username=username)
    if len(filterResult)>0:
        return JsonResponse({"success":False, "msg":"Duplicated username."})

    user = UserInfo()
    user.username = username
    user.password = password
    user.email = email
    user.save()

    connect = ConnectUser()
    connect.username = username
    connect.uuid = uuid.uuid4()
    connect.save()

    return JsonResponse({"success": True, "token":connect.uuid, 'user_name': username, 'user_email': email})

#用户登录
def userlogin(request):
    if request.method=='POST':
        username=request.POST.get('username','')
        password=request.POST.get('userpwd','')

    user=UserInfo.objects.filter(username=username)
    if len(user)==0: #用户名不存在
        return JsonResponse({"success": False, "msg": "User does not exist."})
    elif user[0].password != password:
        return JsonResponse({"success": False, "msg": "Password error."})
    else:
        check = ConnectUser.objects.filter(username=username)
        if len(check) > 0:
            return JsonResponse({"success": True, "token": check[0].uuid, 'user_name': username, 'user_email': user[0].email})
        connect = ConnectUser()
        connect.username = username
        connect.uuid = uuid.uuid4()
        connect.save()
        return JsonResponse({"success": True, "token": connect.uuid, 'user_name': username, 'user_email': user[0].email})

#用户注销
def userlogout(request):
    if request.method=='POST':
        uuid=request.POST.get('uuid','')
    user=ConnectUser.objects.filter(uuid=uuid)
    if len(user)==0:
        return JsonResponse({"success": False, 'msg': "uuid Error. "})
    else:
        user[0].delete()
        return JsonResponse({"success": True})

#修改密码
def change_pwd(request):
    if request.method=='POST':
        uuid=request.POST.get('uuid','')
        username=ConnectUser.objects.filter(uuid=uuid)
        if len(username)==0:
            return JsonResponse({"success":False, "msg":"Invalid uuid."})
        pwd=request.POST.get('userpwd','')
        user=UserInfo.objects.filter(username=username[0])
        if len(user)==0:
            return JsonResponse({"success":False, "msg":"Unknow error."})
        user.password=pwd
        user.save()
        return JsonResponse({"success":True, "msg":"Success."})

#搜索站内课程
def course_list(request):
    if request.method=='POST':
        keyword=request.POST.get('key','')
        max_size=request.POST.get('max_size','')
        querycourse=CourseInfo.objects.filter(Q(course_name__contains=keyword)|Q(teacher_name__contains=keyword)|Q(course_info__contains=keyword))
        courselist=[]
        for i in range(min(len(querycourse), int(max_size))):
            courselist.append({'course_id': querycourse[i].id,
                               'course_name': querycourse[i].course_name,
                               'course_info': querycourse[i].course_info,
                               'user_id': querycourse[i].teacher_id,
                               'user_name': querycourse[i].teacher_name,
                               'jwb_credit': querycourse[i].jwb_credit,
                               'amount': querycourse[i].amount,
                               'create_time': querycourse[i].time.strftime("%Y-%m-%d %H:%I:%S")})  # 发布课程的时间

        return JsonResponse({'course_list': courselist, 'len': min(len(querycourse), int(max_size))})

def check_connect(uuid):
    user=ConnectUser.objects.filter(uuid=uuid)
    if len(user)==0:
        return 'invalid'
    else:
        return user[0].username

#发布新课程
def create_course(request):
    if request.method=='POST':
        uuid=request.POST.get('uuid','')
        username=check_connect(uuid)
        if username=='invalid':
            return JsonResponse({'Success':False, 'msg': 'Invalid uuid. '})

        course = CourseInfo()
        course.course_name = request.POST.get('course_name','')
        course.course_info = request.POST.get('course_info', '')
        course.teacher_id = UserInfo.objects.filter(username=username)[0].id
        course.teacher_name = username
        course.jwb_credit = request.POST.get('jwb_credit', '')
        course.amount = int(request.POST.get('amount', ''))
        if course.amount < 0:
            return JsonResponse({'Success': False, 'msg': 'Invalid amount. '})
        #course.time = timezone.now()
        course.save()

        return JsonResponse({'Success':True, 'course_id': course.id})

#教师删除课程
def delete_course(request):
    if request.method=='POST':
        uuid = request.POST.get('uuid','')
        username = check_connect(uuid)
        if username == 'invalid':
            return JsonResponse({'Success': False, 'msg': 'Invalid uuid. '})

        user = UserInfo.objects.filter(username=username)[0]
        course_id = request.POST.get('course_id', '')
        course = CourseInfo.objects.filter(id=course_id)[0]

        if course.teacher_id != user.id:#不是开课的教师
            return JsonResponse({'Success': False, 'msg': 'Permission denied. '})

        orderlist=OrderInfo.objects.filter(course_id=course_id)
        for i in range(len(orderlist)):
            orderlist[i].order_state = '2' #state=2： 对应课程已删除
            orderlist[i].save()

        course.delete()
        return JsonResponse({'Success': True})

#查看用户出售课程
def sell_course(request):
    if request.method=='POST':
        uuid=request.POST.get('uuid','')

        username = check_connect(uuid)
        if username == 'invalid':
            return JsonResponse({'Success': False, 'msg': 'Invalid uuid. '})

        userid=UserInfo.objects.filter(username=username)[0].id
        querycourse = CourseInfo.objects.filter(teacher_id=userid)
        courselist=[]
        for i in range(len(querycourse)):
            courselist.append({'course_id':querycourse[i].id,
                               'course_name':querycourse[i].course_name,
                               'course_info':querycourse[i].course_info,
                               'user_id':querycourse[i].teacher_id,
                               'user_name':querycourse[i].teacher_name,
                               'jwb_credit':querycourse[i].jwb_credit,
                               'amount':querycourse[i].amount,
                               'create_time':querycourse[i].time.strftime("%Y-%m-%d %H:%I:%S")})#发布课程的时间

        return JsonResponse({'course_list':courselist, 'len':len(courselist)})

#查看用户购买课程
def buy_course(request):
    if request.method=='POST':
        uuid=request.POST.get('uuid','')
        username = check_connect(uuid)
        if username == 'invalid':
            return JsonResponse({'Success': False, 'msg': 'Invalid uuid. '})

        user = UserInfo.objects.filter(username=username)[0]
        queryorder = OrderInfo.objects.filter(student_id=user.id)

        courselist=[]
        for i in range(len(queryorder)):
            a_course = CourseInfo.objects.filter(id=queryorder[i].course_id)

            if len(a_course)==0: #对应的课程已被删除
                courseinfo = 'Course has been deleted. '
            else:
                courseinfo = a_course[0].course_info
            courselist.append({'order_id': queryorder[i].id,
                               'course_info': courseinfo,
                               'order_info': queryorder[i].order_info,
                               'order_state': queryorder[i].order_state,
                               'course_id': queryorder[i].course_id,
                               'course_name': queryorder[i].course_name,
                               'student_id': queryorder[i].student_id,
                               'student_name': queryorder[i].student_name,
                               'student_info': user.info,
                               'teacher_id': queryorder[i].teacher_id,
                               'teacher_name': queryorder[i].teacher_name,
                               'create_time': queryorder[i].time.strftime("%Y-%m-%d %H:%I:%S")})

        return JsonResponse({'order_list':courselist, 'len':len(courselist)})

#查看某课程的订单
def order_list(request):
    if request.method=='POST':
        courseid=request.POST.get('course_id','')
    findorder=OrderInfo.objects.filter(course_id=courseid)

    returnlist=[]
    for i in range(len(findorder)):
        courseinfo=CourseInfo.objects.filter(id=findorder[i].course_id)[0]
        teacherinfo=UserInfo.objects.filter(id=findorder[i].teacher_id)[0]
        studentinfo = UserInfo.objects.filter(id=findorder[i].teacher_id)[0]
        returnlist.append({'order_id':findorder[i].id,
                           'order_info':findorder[i].order_info,
                           'order_state':findorder[i].order_state,
                           'course_id':findorder[i].course_id,
                           'course_name':courseinfo.course_name,
                           'student_id':studentinfo.id,
                           'student_name':studentinfo.username,
                           'student_info': studentinfo.info,
                           'teacher_id':teacherinfo.id,
                           'teacher_name':teacherinfo.username,
                           'course_info':courseinfo.course_info,
                           'amount': courseinfo.amount,
                           'create_time':(timezone.now() - findorder[i].time).seconds})

    return JsonResponse({'order_list':returnlist, 'len':len(returnlist)})

#修改个人信息
def modify_user_info(request):
    if request.method=='POST':
        uuid = request.POST.get('uuid','')
        user_info = request.POST.get('user_info', '')

        user_name = check_connect(uuid)
        if user_name == 'invalid':
            return JsonResponse({'Success': False, 'msg': 'Invalid uuid. '})

        user = UserInfo.objects.filter(username=user_name)[0]
        user.info = user_info
        return JsonResponse({'Success': True, 'user_info': user_info})

#学生购买课程（创建订单）
def create_order(request):
    if request.method=='POST':
        uuid = request.POST.get('uuid','')
        course_id = request.POST.get('course_id','')
        order_info = request.POST.get('order_info', '')

        user_name = check_connect(uuid)
        if user_name == 'invalid':
            return JsonResponse({'Success': False, 'msg': 'Invalid uuid. '})

        course = CourseInfo.objects.filter(id=course_id)[0]
        student = UserInfo.objects.filter(username=user_name)[0]

        order=OrderInfo()
        order.course_id = course_id
        order.course_name = course.course_name
        order.teacher_id = course.teacher_id
        order.teacher_name = course.teacher_name
        order.student_id = student.id
        order.student_name = student.username
        order.order_info = order_info
        order.order_state = 0
        #order.time = timezone.now()
        order.save()

        return JsonResponse({'Success': True, 'order_id': order.id})

#显示用户信息
def show_userinfo(request):
    if request.method=='POST':
        uuid = request.POST.get('uuid', '')
        username = request.POST.get('username', '')

        if check_connect(uuid) == 'invalid':
            return JsonResponse({'Success': False, 'msg': 'Invalid uuid. '})

        user=UserInfo.objects.filter(username=username)[0]


        return JsonResponse({'Success': True,
                             'user_info':
                                {'user_id': user.id,
                                'user_name': user.username,
                                'email': user.email,
                                'QQnumber': user.QQnumber,
                                'time': user.time.strftime("%Y-%m-%d %H:%I:%S")}
                             })



#回调函数：修改订单状态为已支付
def order_paid(request):
    if request.method=='POST':
        appid = request.POST.get('app_id', '')
        appkey = request.POST.get('app_key', '')
        orderid = request.POST.get('order_id', '')

        check_app = AppVeri.objects.filter(id=appid, app_key=appkey)

        if len(check_app) == 0:
            return JsonResponse({'Success': False, 'msg': 'Authentication failed.'})

        order = OrderInfo.objects.filter(id=orderid)

        if len(order) == 0:
            return JsonResponse({'Success': False, 'msg': 'Can not find this order.'})

        order[0].order_state = 1
        return JsonResponse({'Success': True})



