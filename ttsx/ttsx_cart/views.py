#coding=utf-8
from django.shortcuts import render
from models import *
from django.http import JsonResponse
from django.db.models import Sum
from ttsx_user.views import zhuang
from ttsx_user.models import UserInfo
# Create your views here.

#在购物车添加商品
def add(request):
    try:
        uid = request.session.get('uid')
        # 得到图片的id
        gid = int(request.GET.get('gid'))
        count = int(request.GET.get('count','1'))

        carts = CartInfo.objects.filter(user_id=uid,goods_id=gid)
        # 如果之前购买过此商品,走这条路径
        if len(carts) == 1:
            cart = carts[0]
            cart.count += count
            cart.save()
        # 如果是第一次购买的话,先创建一个实例对象进行保存
        else:
            cart = CartInfo()
            cart.user_id = uid
            cart.goods_id = gid
            cart.count = count
            cart.save()
        return JsonResponse({'isadd':1})
    except:
        return JsonResponse({'isadd':0})

#统计商品的数量，可以统计购买商品种类的数量也可以商品总个数
def count(request):
    uid = request.session.get('uid')
    # 表示购买类几种商品
    # cart_count = CartInfo.objects.filter(user_id=uid).count()
    # 表示购买了多少个商品,aggregate(Sum(变量))返回的是一个字典{'变量__sum':number}
    # 通过get('变量__sum')获取number
    cart_count = CartInfo.objects.filter(user_id=uid).aggregate(Sum('count')).get('count__sum')  # count__sum
    # 当用户第一次登录的时候,未添加任何商品，会输出None
    if cart_count == None:
        cart_count = 0
    return JsonResponse({'cart_count':cart_count})


#添加一个装饰器,在未登录状态的情况下点击购物车,返回登录页登录后，直接跳转到之前的页面
@zhuang
def index(requst):
    uid = requst.session.get('uid')
    # 表示购买类几种商品
    cart_list = CartInfo.objects.filter(user_id=uid)
    context = {'title':'购物车','cart_list':cart_list}
    return render(requst,'ttsx_cart/cart.html',context)


#在购物车页面添加或减少商品数量
def edit(request):
    id = int(request.GET.get('id'))
    count = int(request.GET.get('count'))
    cart = CartInfo.objects.get(pk=id)
    cart.count = count
    cart.save()
    return JsonResponse({'ok':1})


#在购物车删除某个选中的商品
def delete(request):
    id = int(request.GET.get('id'))
    cart = CartInfo.objects.get(pk=id)
    cart.delete()
    return JsonResponse({'ok':1})


# 结算订单视图
def order(request):
    # 通过之前记录的uid获取用户登录信息,通过id在用户表查到相应的用户
    user = UserInfo.objects.get(pk=request.session.get('uid'))
    # 在购物车的模板中把内容放到表单中,通过post请求获得提交的内容(即购物车选中的商品)
    cart_ids = request.POST.getlist('cart_id')
    c_ids = ','.join(cart_ids) #将列表转换为字符串
    # in：是否包含在范围内
    cart_list = CartInfo.objects.filter(id__in=cart_ids)
    context = {'title': '提交订单', 'user': user, 'cart_list': cart_list,'c_ids':c_ids}
    return render(request, 'ttsx_cart/order.html', context)