"""PT_TutorMall_Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from server import views as sv

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', sv.userlogin, name='login'),
    url(r'^logout/', sv.userlogout, name='logout'),
    url(r'^register/', sv.UserRegister, name='register'),
    url(r'^create_course/', sv.create_course, name='create_course'),
    url(r'^course_list/', sv.course_list, name='course_list'),
    url(r'^sell_course/', sv.sell_course, name='sell_course'),
    url(r'^buy_course/', sv.buy_course, name='buy_course'),
    url(r'^order_list/', sv.order_list, name='order_list'),
    url(r'^create_order/', sv.create_order, name='create_order'),
    url(r'^modify_user_info/', sv.modify_user_info, name='modify_user_info')
]
