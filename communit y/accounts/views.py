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
    hasLogin=False
    if request.user.is_authenticated:  #django自带的一个判断是否为已登陆请求的方法
        user=request.user
        userProfile=BlogUser.objects.get(user=user)
        hasLogin=True
    else:
        userProfile=[]
    data={'userProfile':userProfile,'hasLogin':hasLogin}
    return render(request, 'accounts/index.html',data)
@csrf_exempt
def register(request):
    if request.method == 'GET':
        userForm = UserForm()
        profileForm = UserProfileForm()
        data={'userForm':userForm,'profileForm':profileForm,}
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
            req={'message':'success','reason':'注册成功'}
            return HttpResponse(dumps(req),content_type="application/json")
        else:
            req={'message':'fail','reason':'未接收到正确的表单,或创建过程中出错'}
            return HttpResponse(dumps(req),content_type="application/json")

@csrf_exempt
def user_login(request):
    if request.method == 'GET':
        data={}
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
    logout(request)
    req={'message':'success','reason':'登出成功'}
    return HttpResponse(dumps(req),content_type="application/json")

@csrf_exempt
def resetpassword(request):
    if request.method == 'GET':
        data={}
        return render(request, 'accounts/login.html', data)
    # elif request.method == 'POST':
    #     uf = ResetPassForm(request.POST)
    #     if uf.is_valid():
    #         #获得表单数据
    #         username = uf.cleaned_data['username']
    #         password = uf.cleaned_data['password']
    #         newPassword = uf.cleaned_data['newpassword']
    #         #判断数据格式
    #         if password == '':
    #             req={'message':'fail','reason':'请填写密码'}
    #             return HttpResponse(dumps(req),content_type="application/json")
    #         #判断密码是否正确
    #         if username != '':
    #             res = BlogUser.objects.filter(username = username,password = password)
    #             if res:
    #                 res.password=newPassword
    #                 res.save()
    #                 req={'message':'success','reason':'修改成功'}
    #                 return HttpResponse(dumps(req),content_type="application/json")
    #             else:
    #                 req={'message':'fail','reason':'密码与用户名不符'}
    #                 return HttpResponse(dumps(req),content_type="application/json")
    #         else:
    #             req={'message':'fail','reason':'请填写用户名'}
    #             return HttpResponse(dumps(req),content_type="application/json")
    #     else:
    #         req={'message':'fail','reason':'表单错误,无法接收到正确的信息'}
    #         return HttpResponse(dumps(req),content_type="application/json")

    # else:
    #     req={'message':'fail','reason':'请求方式错误'}
    #     return HttpResponse(dumps(req),content_type="application/json")


@csrf_exempt
def getUserInfo(request):

    return HttpResponse('todo')