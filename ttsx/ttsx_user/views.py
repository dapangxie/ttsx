#coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse
import datetime

# Create your views here.


#跳转到注册页面
def register(request):
    context = {'title':'注册','top':'0'}
    return render(request,'ttsx_user/register.html',context)


#获取用户注册信息,将用户信息存入数据库,并对密码进行shal1加密,
#并跳转到登录界面
def register_handle(request):
    #获取输入的值
    p = request.POST
    uname = p.get('user_name')
    upwd = p.get('user_pwd')
    umail = p.get('user_email')
    #对密码进行加密
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()

    #获取对象,保存到数据库
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd_sha1
    user.umail = umail
    user.save()
    return redirect('/user/login/')


#在注册时判断用户是否已经注册
def register_estimate(request):
    uname = request.GET.get('uname')
    result = UserInfo.objects.filter(uname=uname).count()
    context = {'valid':result}
    return JsonResponse(context)


#跳转到登录界面
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title':'登录','uname':uname,'top':'0'}
    return render(request,'ttsx_user/login.html',context)


def login_handle(request):
    #得到用户输的用户名和密码
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('user_pwd')
    uname_jz = post.get('name_jz','0')
    #对用户输入的用户名进行加密
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()

    #如果用户名错误,提交以后将显示在页面上
    context = {'title':'登录','uname':uname,'upwd':upwd,'top':'0'}
    #如果用户名存在,返回users=[<UserInfo: python>],不存在的话[]一个空的列表
    users = UserInfo.objects.filter(uname=uname)
    # print users
    # print users[0]
    if len(users) == 0:
        #表示用户名不存在
        context['name_error'] = '1'
        return render(request,'ttsx_user/login.html',context)
    else:
        if users[0].upwd == upwd_sha1:
            #记住登录用户
            request.session['uname'] = users[0].uname
            request.session['uid'] = users[0].id
            #记住用户名
            path=request.session.get('url_path','/')
            response=redirect(path)
            if uname_jz == '1':
                response.set_cookie('uname', uname, expires=datetime.datetime.now() + datetime.timedelta(days=7))
            #不想记住用户名
            else:
                response.set_cookie('uname','',max_age=-1)
            return response
        else:
            context['pwd_error'] = '1'
            return render(request,'ttsx_user/login.html',context)


#清除路径
def logout(request):
    request.session.flush()
    return redirect('/user/login/')

#定义一个装饰器
def zhuang(func):
    def log(request,*args,**kwargs):
        # 判断用户是否登录
        if request.session.has_key('uid'):
            # 如果登录，则继续执行视图
            return func(request,*args,**kwargs)
        else:
            # 如果没登录，则转到登录页
            return redirect('/user/login/')
    return log

#center = zhuang(center)
@zhuang
#用户中心
def center(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    context = {'title':'用户中心','user':user}
    return render(request,'ttsx_user/center.html',context)

@zhuang
#订单
def order(request):
    context = {'title':'用户订单'}
    return render(request,'ttsx_user/order.html',context)

@zhuang
#收货地址
def site(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    if request.method == 'POST':
        #获取输入的内容
        post = request.POST
        ushou = post.get('ushou')
        uphone = post.get('uphone')
        uaddress = post.get('uaddress')

        #将输入的内容保存到数据库
        user.ushou = ushou
        user.uphone = uphone
        user.uaddress = uaddress
        user.save()

    context = {'title': '收货地址','user':user}
    return render(request, 'ttsx_user/site.html', context)



