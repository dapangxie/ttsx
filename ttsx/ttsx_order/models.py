#coding=utf-8
from django.db import models
from ttsx_user.models import UserInfo
from ttsx_goods.models import GoodsInfo
# Create your models here.


# 主订单 当有字段一开始未传内容时要设定默认值
class OrderMain(models.Model):
    # 表示id primary_key：若为True，则该字段会成为模型的主键字段,需自己手动添加
    order_id = models.CharField(max_length=20,primary_key=True)#年/月/日/uid
    # 用户表和用户是一对多关系,ForeignKey：一对多，将字段定义在多的一端中
    user = models.ForeignKey(UserInfo)
    # 下单日期,参数auto_now_add表示当对象第一次被创建时自动设置当前时间，用于创建的时间戳，它总是使用当前日期
    order_date = models.DateTimeField(auto_now_add=True)
    # 表示总支付金额,DecimalField十进制浮点数
    # max_digits表示总位数,decimal_places表示小数位数
    total = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    # 订单状态，已支付还是未支付
    state = models.IntegerField(default=0)


# 详细订单
class OrderDetail(models.Model):
    order = models.ForeignKey(OrderMain)
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=5,decimal_places=2)