# File:urls.py
# Copyright(C) OldTaoge 2020.All rights reserved.
# By GPL v3.0
from django.urls import path

from . import views

app_name = 'xxtj'
urlpatterns = [
    # path('', views.index, name='index'),
    # path('', views.index, name='index'),
    path('index/<int:class_id>/', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('result/', views.result, name='result'),
    path('result_group/', views.result_group, name='result_group'),
    path('ajax/', views.ajax, name='ajax'),
    path('file/', views.file, name='file'),
]