from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Post,Comment
from accounts.models import BlogUser
from django.views.decorators.csrf import csrf_exempt
from json import dumps
from .forms import CommentForm,PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    '''
    主页
    '''
    postList=[]
    for i in Post.objects.all():
        postList.append(i.title)
    data={'postList':postList}

    #验证是否登陆
    if request.user.is_authenticated:
        user=request.user
        hasLogin=True
    else:
        hasLogin=False
        user=False
    data['hasLogin']=hasLogin
    return render(request, 'posting/index.html', data)

def getPostByTitle(request,postTitle):
    '''
    查看帖子
    '''
    if request.method == 'GET':
        post=Post.GetPost(title=postTitle)
        if post=='查询错误':
            html='查询错误'
            return HttpResponse(html)

        comment = post.comment_set.all() #评论集
        comment = comment.order_by('-createDate') #按照发送时间排序
        commentForm = CommentForm()

        data={
            'post':post,
            'comment':comment,
            'commentForm':commentForm,
        }
        #验证是否登陆
        if request.user.is_authenticated:
            user=request.user
            hasLogin=True
        else:
            hasLogin=False
            user=False
        data['hasLogin']=hasLogin
        return render(request, 'posting/post.html', data)
    elif request.method == 'POST':
        createComment(request)
    else:
        req={'message':'fail','reason':'请求方式错误'}
        return HttpResponse(dumps(req),content_type="application/json")


@csrf_exempt
@login_required
def createComment(request,postId):
    '''
    添加评论
    只有登陆后才能登陆
    '''
    if request.method == 'POST':
        commentForm=CommentForm(request.POST)
        if commentForm.is_valid():
            try:
                post1=Post.objects.get(pk=postId)
                username=BlogUser.objects.get(user=request.user)
                Comment(username=username,body=request.POST['body'],post=post1).save()
            except:
                req={'message':'fall','reason':'该帖子不存在或被删除,无法回复'}
                return HttpResponse(dumps(req),content_type="application/json")

            req={'message':'success','reason':'评论成功'}
            return HttpResponse(dumps(req),content_type="application/json")
        else:
            req={'message':'fail','reason':'未接收到正确的表单,或创建过程中出错'}
            return HttpResponse(dumps(req),content_type="application/json")

    else:
        req={'message':'fail','reason':'请求方式失败'}
        return HttpResponse(dumps(req),content_type="application/json")

@login_required
@csrf_exempt
def createPosting(request):
    '''
    创建帖子
    '''
    if request.method == 'POST':  #post请求创建post
        postForm=PostForm(request.POST)
        if postForm.is_valid():
            postForm=postForm.save(commit=False)
            user=BlogUser.objects.get(user=request.user)
            postForm.author=user
            postForm.save()
            req={'message':'success','reason':'发帖成功'}
            return HttpResponse(dumps(req),content_type="application/json")
        else:
            req={'message':'fail','reason':'发帖失败'}
            return HttpResponse(dumps(req),content_type="application/json")


    elif request.method == 'GET':  #get请求返回页面
        postForm = PostForm()
        data={
            'postForm':postForm,
        }
        #验证是否登陆
        if request.user.is_authenticated:
            user=request.user
            hasLogin=True
        else:
            hasLogin=False
            user=False
        data['hasLogin']=hasLogin
        return render(request, 'posting/createPost.html', data)
    else:
        req={'message':'fail','reason':'请求方式错误'}
        return HttpResponse(dumps(req),content_type="application/json")