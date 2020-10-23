# File:urls.py
# Copyright(C) OldTaoge 2020.All rights reserved.
# By GPL v3.0
from django.urls import path

from . import views

app_name = 'advance'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('', views.index, name='index'),
    path('cla_inf/', views.cla_inf, name='cla_inf'),
    path('add_cla/', views.add_cla, name='add_cla'),
    path('del_cla/', views.del_cla, name='del_cla'),
    path('edit_cla/', views.edit_cla, name='edit_cla'),
    path('stu_inf/', views.stu_inf, name='stu_inf'),
    path('add_stu/', views.add_stu, name='add_stu'),
    path('del_stu/', views.del_stu, name='del_stu'),
    path('edit_stu/', views.edit_stu, name='edit_stu'),
    path('sta_inf/', views.sta_inf, name='sta_inf'),
    path('add_sta/', views.add_sta, name='add_sta'),
    path('del_sta/', views.del_sta, name='del_sta'),
    path('edit_sta/', views.edit_sta, name='edit_sta'),
    # path('adm_ind/', views.adm_ind, name='adm_inf'),
    path('personal/', views.personal, name='personal'),
    path('change_password', views.change_password, name='change_password'),
    path('account_console/', views.account_console, name='account_console'),
    path('account_console/add_admin/', views.account_console_add_admin, name='account_console.add_admin'),
    path('account_console/del_admin/', views.account_console_del_admin, name='account_console.del_admin'),
    path('account_console/edit_admin/', views.account_console_edit_admin, name='account_console.edit_admin'),
    path('account_console/result/', views.account_console_result, name='account_console.result'),
    path('ajax/', views.ajax, name='ajax')
]
