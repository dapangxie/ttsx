#coding=utf-8
from django.db import models
from hashlib import sha1

# Create your models here.


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)  #用户名
    upwd = models.CharField(max_length=40)  #用户密码
    umail = models.CharField(max_length=20) #邮件
    uphone = models.CharField(default='',max_length=11)  #电话
    uaddress = models.CharField(default='',max_length=100)  #收件地址
    ushou = models.CharField(default='',max_length=20)   #收件人
    ucode = models.CharField(default='',max_length=10)   #邮编
    # def __str__(self):
    #     return self.uname