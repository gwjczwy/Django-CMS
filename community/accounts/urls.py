from django.urls import path
from . import views

app_name='accounts'
urlpatterns=[
    path('user/',views.index),
    path('user/register/',views.register),
    path('user/login/',views.user_login),
    path('user/logout/',views.user_logout),
    path('user/resetpassword/',views.resetpassword),
    #纯后端接口
    path('user/getUserInfo/',views.getUserInfo),
        

]