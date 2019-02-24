from django.db import models
from django.utils.timezone import now #当前时间
from accounts.models import BlogUser #导入django内建user模型

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(BlogUser,on_delete=models.CASCADE)
    title = models.CharField('标题', max_length=200, unique=True)
    body = models.TextField('正文')
    createDate = models.DateTimeField('创建时间', default=now)
    updateDate = models.DateTimeField('修改时间', default=now)
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-createDate']

    def GetPost(title=''):
        try:
            s=Post.objects.get(title=title)
            s.createDate=str(s.createDate)
            return s
        except:
            return '查询错误'


class Comment(models.Model):
    name = models.CharField('名称',max_length=50)
    body = models.TextField('评论内容')
    createDate = models.DateTimeField('创建时间', default=now)
    updateDate = models.DateTimeField('修改时间', default=now)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)


    def __str__(self):
        return self.body
    class Meta:
        ordering = ['createDate']

