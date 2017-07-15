#coding=utf-8
from django.db import models
from ttsx_user.models import UserInfo
from ttsx_goods.models import GoodsInfo

# Create your models here.

class CartInfo(models.Model):
    # 购买的用户,用户表和用户是一对多的关系(ForeignKey),把字段定义在多的一端
    user = models.ForeignKey(UserInfo)
    # 购买的商品,商品列表和商品是一对多的关系(ForeignKey),把字段定义在多的一端
    goods = models.ForeignKey(GoodsInfo)
    # 表示购买数量或者是商品总数
    count = models.IntegerField()

