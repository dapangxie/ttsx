#coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
from haystack.generic_views import SearchView
# Create your views here.


def index(request):
    goods_list=[]#[{},{},{}]===>{'typeinfo':,'new_list':,'click_list':}
    #查询分类对象
    #查询每个分类中最新的4个商品
    #查询每个分类中最火的4个商品
    type_list=TypeInfo.objects.all()
    for t1 in type_list:
        nlist=t1.goodsinfo_set.order_by('-id')[0:4]
        clist=t1.goodsinfo_set.order_by('-gclick')[0:3]
        goods_list.append({'t1':t1,'nlist':nlist,'clist':clist})
    context={'title':'首页','glist':goods_list,'car_show':'1'}
    return render(request,'ttsx_goods/index.html',context)


def list(request,tid,pindex,orderby):
    try:
        t1 = TypeInfo.objects.get(pk=int(tid))
        new_list = t1.goodsinfo_set.order_by('-id')[0:2]

        #指定规则排序
        orderby_str = '-id'
        desc = '1'
        #根据价格排序
        if orderby == '2':
            desc = request.GET.get('desc','1')
            #价格通过倒序排列
            if desc == '1':
                orderby_str = '-gprice'
            else:
                orderby_str = 'gprice'
        #按照点击量排序
        elif orderby_str == '3':
            orderby_str = '-gclick'

        # 查询：当前分类的所有商品，按每页15个来显示
        glist = t1.goodsinfo_set.order_by(orderby_str)
        paginator = Paginator(glist, 3)
        pindex1 = int(pindex)
        if pindex1 < 1:
            pindex1 = 1
        elif pindex1 > paginator.num_pages:
            pindex1 = paginator.num_pages
        page = paginator.page(pindex1)
        print page
        context = {'title': '商品列表页', 'car_show': '1', 't1': t1, 'new_list': new_list, 'page': page,'orderby':orderby,'desc':desc}
        return render(request, 'ttsx_goods/list.html', context)
    except:
        return render(request, '404.html')


def detail(request,id):
    # try:
        goods=GoodsInfo.objects.get(pk=int(id))
        goods.gclick+=1
        goods.save()
        new_list=goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context={'title':'商品详细页','car_show':'1','goods':goods,'new_list':new_list}
        response = render(request,'ttsx_goods/detail.html',context)
        #保存最近浏览[1,2,3,4,5]<===>'1,2,3,4,5'  ','.join()   .split()
        #步骤: 先读取已经存在的->>进行拼接->>输出
        #将字符串拼接成列表
        gids = request.COOKIES.get('goods_ids','').split(',')
        #判断这个编号是否存在，如果存在则删除，然后再加到最前面
        if id in gids:
            gids.remove(id)
        gids.insert(0,id)
        #如果超过5个，则删除最后一个
        if len(gids)>6:
            gids.pop()
        # response.set_cookie('goods_ids',',.join(gids),',max_age = 60*60*24*7)
        response.set_cookie('goods_ids', ','.join(gids), max_age=60 * 60 * 24 * 7)
        return response
    # except:
    #     return render(request,'404.html')


class MySearchView(SearchView):
    # 自定义搜索视图,从haystack官方文档中查看
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        # 判断继承base模板下的那个区域
        context['car_show'] = '1'
        page_range = []
        # 查看你的模板并用page变量替换page_obj,context已字典的形式存储，
        # 通过得到模板中的键page_obj获取值
        page = context.get('page_obj')
        # page对象下的paginator属性，当前页对应的Paginator对象,
        # Paginator对象下的num_pages属性返回总页数
        if page.paginator.num_pages<5:
            # Paginator对象下的page_range属性返回返回页码列表，从1开始，例如[1, 2, 3, 4]
            page_range = page.paginator.page_range
        # 表示第1页和第2页
        elif page.number <= 2:
            page_range = range(1,6)
        # page.paginator.num_pages表示总页数
        elif page.number >= page.paginator.num_pages-1:
            page_range = range(page.paginator.num_pages-4,page.paginator.num_pages+1)
        else:# 3 4 5 6 7
            page_range=range(page.number-2,page.number+3)
        context['page_range']=page_range
        print len(page_range)
        return context
