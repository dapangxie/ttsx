#coding=utf-8
from django.conf.urls import url
import views

urlpatterns = [
    url(r'^add/$',views.add),
    url(r'^count/$',views.count),
    url(r'^$',views.index),
    url(r'^edit/$',views.edit),
    url(r'^del/$',views.delete),
    url(r'^order/$',views.order),
]