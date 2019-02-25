from django.db import models
from django.utils.timezone import now #当前时间
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

GENDER = {
            ('m','man'),
            ('w','woman'),
            ('s','secret')
        }

class BlogUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,default=None, null=True)
    nickname = models.CharField('昵称', max_length=100, blank=True)
    mugshot = models.ImageField('头像', upload_to='upload/mugshots', blank=True)
    lastLoginDate = models.DateTimeField('最后一次登陆', default=now)
    icon = models.IntegerField('硬币数量',default=0)
    # lastLoginIP = models.GenericIPAddressField('最后一次登陆地址')
    telephone = models.CharField('电话号码',max_length = 15,default='')
    gender = models.CharField('性别',max_length=1,choices=GENDER,default='s')

    def __str__(self):
        return self.user.username