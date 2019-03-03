from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import BlogUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login,logout
from json import dumps
from .forms import UserForm,UserProfileForm
from django.contrib.auth.decorators import login_required


def index(request):
    '''
    个人信息页面
    如果登陆了就显示个人信息等信息
    没有登陆则是一个空白界面
    '''
    if request.user.is_authenticated:
        user=request.user
        hasLogin=True
    else:
        hasLogin=False
        user=False
    if request.user.is_authenticated:  #django自带的一个判断是否为已登陆请求的方法
        user=request.user
        userProfile=BlogUser.objects.get(user=user)
        hasLogin=True
    else:
        userProfile=[]
    data={'userProfile':userProfile,'hasLogin':hasLogin,'user':user}
    return render(request, 'accounts/index.html',data)
@csrf_exempt
def register(request):
    '''
    注册账号
    '''
    if request.method == 'GET':
        if request.user.is_authenticated:
            user=request.user
            hasLogin=True
        else:
            hasLogin=False
            user=False
        userForm = UserForm()
        profileForm = UserProfileForm()
        data={'userForm':userForm,'profileForm':profileForm,'hasLogin':hasLogin,'user':user}
        return render(request, 'accounts/register.html', data)
    elif request.method == 'POST':
        userForm = UserForm(request.POST)
        userProfileForm = UserProfileForm(request.POST)
        if userForm.is_valid() and userProfileForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            profile=userProfileForm.save(commit=False)
            profile.user = user
            if 'mugshot' in request.FILES:
                profile.mugshot = request.FILES['mugshot']
            profile.save()
            # user_login(request)
            return HttpResponseRedirect('/user/')
        else:
            req={'message':'fail','reason':'未接收到正确的表单,或创建过程中出错'}
            return HttpResponse(dumps(req),content_type="application/json")

@csrf_exempt
def user_login(request):
    '''
    用户登陆页面
    登陆的后台逻辑
    '''
    if request.method == 'GET':
        if request.user.is_authenticated:
            user=request.user
            hasLogin=True
        else:
            hasLogin=False
            user=False
        data={'hasLogin':hasLogin,'user':user}
        return render(request, 'accounts/login.html', data)
    elif request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                req={'message':'success','reason':'登陆成功'}
                return HttpResponse(dumps(req),content_type="application/json")
            else:
                req={'message':'fail','reason':'该用户以被禁止登陆'}
            return HttpResponse(dumps(req),content_type="application/json")
        else:
            req={'message':'fail','reason':'错误的用户名和密码'}
            return HttpResponse(dumps(req),content_type="application/json")

@login_required
def user_logout(request):
    '''
    用户登出
    '''
    logout(request)
    return HttpResponseRedirect('/user/login')

@csrf_exempt
@login_required
def resetpassword(request):
    '''
    重置密码
    '''
    if request.method == 'GET':
        if request.user.is_authenticated:
            user=request.user
            hasLogin=True
        else:
            hasLogin=False
            user=False
        data={'hasLogin':hasLogin,'user':user}
        return render(request, 'accounts/resetpassword.html', data)
    elif request.method == 'POST':
        user=request.user
        user.set_password(request.POST['password'])
        user.save()
        req={'message':'success','reason':'更改成功'}
        return HttpResponse(dumps(req),content_type="application/json")
    else:
        req={'message':'fall','reason':'请求方式错误'}
        return HttpResponse(dumps(req),content_type="application/json")
        


@csrf_exempt
def getUserInfo(request):
    '''
    获取用户信息
    '''
    return HttpResponse('todo')