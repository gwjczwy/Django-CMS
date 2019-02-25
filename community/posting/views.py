from django.shortcuts import render
from django.http import HttpResponse
from .models import Post,Comment
from django.views.decorators.csrf import csrf_exempt
from json import dumps

# Create your views here.

def index(request):
    html = "<html><body><h1>index</h1></body></html>"
    return HttpResponse(html)

def getPostByTitle(request,postTitle):
    if request.method == 'GET':
        post=Post.GetPost(title=postTitle)
        if post=='查询错误':
            html='查询错误'
            return HttpResponse(html)

        comment = post.comment_set.all() #评论集
        comment = comment.order_by('-createDate') #按照发送时间排序

        data={
            'post':post,
            'comment':comment
        }

        # return HttpResponse('<h1>查询成功</h1>')
        return render(request, 'posting/post.html', data)

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




        

