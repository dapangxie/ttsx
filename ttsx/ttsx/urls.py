#coding=utf-8
"""ttsx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # 用于后台站点管理
    url(r'^admin/', include(admin.site.urls)),
    # 用户应用
    url(r'^user/', include('ttsx_user.urls')),
    # 商品应用
    url('^',include('ttsx_goods.urls')),
    # 富文本编辑器路径
    url(r'^tinymce/', include('tinymce.urls')),
    # 全文检索路径,当自定义搜索的时候这条就不用了
    # url(r'^search/', include('haystack.urls')),
    # 购物车应用
    url('^cart/',include('ttsx_cart.urls')),
    # 用于全部订单提交
    url(r'^order/',include('ttsx_order.urls')),
]
