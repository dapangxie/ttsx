#coding=utf-8
from django.db import models
from tinymce.models import HTMLField
# Create your models here.


class TypeInfo(models.Model):
    ttitle=models.CharField(max_length=20)
    isDelete=models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle.encode('utf-8')


class GoodsInfo(models.Model):
    gtitle=models.CharField(max_length=50)  #商品名称
    gpic=models.ImageField(upload_to='goods')  #商品图片
    gprice=models.DecimalField(max_digits=5,decimal_places=2)#999.99  #商品单价
    gclick = models.IntegerField(default=0)  #点击量
    gunit=models.CharField(max_length=20)   #单位
    isDelete = models.BooleanField(default=False)   #逻辑删除
    gsubtitle=models.CharField(max_length=200)  #商品描述
    gkucun = models.IntegerField(default=100)   #库存
    gcontent=HTMLField()    #富文本编辑器
    gtype=models.ForeignKey('TypeInfo')    #外键
