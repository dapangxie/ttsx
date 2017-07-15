#coding=utf-8
from django.shortcuts import render,redirect
from django.db import transaction
from models import *
from datetime import datetime
from ttsx_cart.models import CartInfo
# Create your views here.
'''
1 创建订单主表
2 接收所有的购物车请求
3 查询到请求的购物车信息
4 逐个判断库存
5 如果库存足够:
    5.1 创建订单祥单
    5.2 改变库存
    5.3 计算总金额
    5.4 删除购物车数据
6 如果库存不够,则放弃之前的保存,转到购物车
'''


@transaction.atomic  #加这个装饰器为了手动提交事物
def do_order(request):
    # 设置一个默认值
    isok = True
    # 创建一个节点，用于事物的提交commit和回滚rollback
    sid = transaction.savepoint()
    try:
        # 获取用户信息
        uid = request.session.get('uid')
        #1创建订单主表
        now_str = datetime.now().strftime('%Y%m%d%H%M%S')
        main = OrderMain()
        main.order_id = '%s%d'%(now_str,uid)
        main.user_id = uid
        main.save()
        #2接收所有购物车请求,并将请求到的信息字符串转换为列表
        cart_ids = request.POST.get('cart_ids').split(',')
        #3查询到请求的购物车信息 in：是否包含在范围内
        cart_list = CartInfo.objects.filter(id__in=cart_ids)
        total = 0
        #4逐个判断库存
        for cart in cart_list:
            #5如果库存足够
            if cart.count <= cart.goods.gkucun:
                #5.1创建订单祥单
                detail = OrderDetail()
                # 表示这个祥单是属于那个订单的
                detail.order = main
                detail.goods = cart.goods
                detail.count = cart.count
                detail.price = cart.goods.gprice
                detail.save()
                #5.2 改变库存
                cart.goods.gkucun -= cart.count
                cart.goods.save()
                #5.3计算金额
                total += cart.count*cart.goods.gprice
                main.total = total
                main.save()
                #5.4删除购物车数据
                cart.delete()
            # 如果库存不够放弃之前的操作,事物回滚到之前的节点
            else:
                isok = False
                transaction.savepoint_rollback(sid)
                break
        if isok:
            transaction.savepoint_commit(sid)
    # except:
    #     transaction.savepoint_rollback(sid)
    #     isok = False
    except:
        transaction.savepoint_rollback(sid)
        isok=False
    # 库存足够,转向订单详细页
    if isok:
        return redirect('/user/order')
    # 否则的话转向购物车
    else:
        return redirect('/cart/')

