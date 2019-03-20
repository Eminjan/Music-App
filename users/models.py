from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,default='',verbose_name='昵称')
    birthday = models.DateField(verbose_name="生日",null=True,blank=True)
    gender = models.CharField(choices=(('male','男'),('female','女')),default='female',verbose_name='性别',max_length=6)
    address = models.CharField(max_length=100,default='',verbose_name='地址')
    mobile = models.CharField(max_length=11,null=True,blank=True,verbose_name='手机')
    avatar = models.ImageField(max_length=100,upload_to='avatar/%Y/%m',default='',verbose_name='头像')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name='邮箱验证码')
    email = models.EmailField(max_length=50,verbose_name='邮箱')

    send_time = models.DateTimeField(default=datetime.now,verbose_name='发送时间')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code, self.email)