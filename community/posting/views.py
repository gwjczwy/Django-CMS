from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Post,Comment
from accounts.models import BlogUser
from django.views.decorators.csrf import csrf_exempt
from json import dumps
from .forms import CommentForm,PostForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    postList=[]
    for i in Post.objects.all():
        postList.append(i.title)
    print(postList)
    data={'postList':postList}
    return render(request, 'posting/index.html', data)

def getPostByTitle(request,postTitle):
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
        req={'message':'请求方式失败'}
        return HttpResponse(dumps(req),content_type="application/json")

@csrf_exempt
def createPosting(request):
    if request.method == 'POST':
        if 'title' not in request.POST or 'body' not in request.POST or 'author' not in request.POST:
            req={'message':'发帖失败','reason':'内容缺失'}
            return HttpResponse(dumps(req),content_type="application/json")
        
        author=request.POST['author']
        body=request.POST['body']
        title=request.POST['title']
        req={'message':'发帖成功'}
        return HttpResponse(dumps(req),content_type="application/json")





        

