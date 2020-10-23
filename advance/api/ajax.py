# File:ajax.py
# Copyright(C) OldTaoge 2020.All rights reserved.
# By GPL v3.0
import json
import os
import shutil
from tongji.settings import get_upload_dir
from django.http import JsonResponse

from xxtj.api.ajax import clear_sta
from xxtj.models import *


def add_cla_ajax(request):
    cla = class_information()
    cla.name_dis = request.GET.get('name_dis')
    cla.person_num = request.GET.get('person_num')
    cla.save()
    return JsonResponse({
        'status': 'success',
    })


def edit_cla_ajax(request):
    cla = class_information.objects.filter(isDelete=False).get(pk=request.GET.get('class_id'))
    cla.name_dis = request.GET.get('name_dis')
    cla.person_num = request.GET.get('person_num')
    cla.save()
    return JsonResponse({
        'status': 'success',
    })


def del_class_ajax(request):
    admin_inf = admin_information.objects.filter().get(pk=request.COOKIES.get('admin_id'))
    if admin_inf.level < 100:
        return JsonResponse({
            'status': 'failure',
            'dis': "权限不够！",
        })
    cla = class_information.objects.filter(isDelete=False).get(pk=request.GET.get('class_id'))
    cla.isDelete = True
    cla.save()
    stu = cla.student_information_set.all()
    for item in stu:
        item.isDelete = True
        item.save()
    sta = cla.statistics_information_set.all()
    for item in sta:
        item.isDelete = True
        item.save()
        rec = item.recond_set.all()
        for foo in rec:
            foo.isDelete = True
            foo.save()
        rec.isDelete = True
    return JsonResponse({
        'status': 'success',
    })


def add_stu_ajax(request):
    stu_name = request.GET.get('stu_name')
    class_id = request.GET.get('class_id')
    stu_inf = student_information()
    stu_inf.student_name = stu_name
    stu_inf.student_class = class_information.objects.filter(isDelete=False).get(pk=class_id)
    stu_inf.save()
    return JsonResponse({
        'status': 'success',
    })


def del_stu_ajax(request):
    admin_inf = admin_information.objects.filter().get(pk=request.COOKIES.get('admin_id'))
    if admin_inf.level < 100:
        return JsonResponse({
            'status': 'failure',
            'dis': "权限不够！",
        })
    stu_id = request.GET.get('stu_id')
    stu_inf = student_information.objects.filter(isDelete=False).get(pk=stu_id)
    stu_inf.isDelete = True
    stu_inf.save()
    return JsonResponse({
        'status': 'success',
    })


def edit_stu_ajax(request):
    stu_id = request.GET.get('stu')
    stu_inf = student_information.objects.filter(isDelete=False).get(pk=stu_id)
    stu_inf.student_name = request.GET.get('stu_name')
    stu_inf.student_class = class_information.objects.filter(isDelete=False).get(pk=request.GET.get('class_id'))

    stu_inf.save()
    return JsonResponse({
        'status': 'success',
    })


def add_sta_ajax(request):
    json_obj = request.POST.get('json')
    json_str = json.loads(json_obj)
    sta_inf = statistics_information()
    sta_inf.statistics_name = json_str["sta_name"]
    sta_inf.statistics_description = json_str["description"]
    sta_inf.statistics_class = class_information.objects.filter(isDelete=False).get(pk=json_str["class_id"])
    if json_str['need_upload']:
        sta_inf.need_upload = True
    sta_inf.save()
    if json_str['need_upload']:
        os.mkdir(get_upload_dir()+str(sta_inf.pk))

    admin_id = []
    for item in json_str['admin_id']:
        admin_id.append(admin_information.objects.filter(isDelete=False).get(pk=item))
    for item in admin_id:
        try:
            obj = admin_statistics.objects.get(admin=item, statistics=sta_inf)
            obj.isDelete = False
        except admin_statistics.DoesNotExist:
            obj = admin_statistics()
            obj.admin = item
            obj.statistics = sta_inf
        obj.save()
    return JsonResponse({
        'status': 'success',
    })


def add_description(json_str):
    json_str = json.loads(json_str)
    # json_str['description']
    for item in json_str['statistics']:
        sta_inf = statistics_information.objects.filter(isDelete=False).get(pk=item)
        sta_inf.statistics_description = str(json_str['description']).replace('\n', '<br>')
        sta_inf.save()
    return JsonResponse({'status': 'success'})


def del_sta_ajax(request):
    admin_id = request.COOKIES.get('admin_id')
    sta_id = request.GET.get('sta_id')
    sta_inf = statistics_information.objects.filter(isDelete=False).get(pk=sta_id)
    admin_id_list = []
    for item in admin_statistics.objects.filter(statistics=sta_inf).filter(isDelete=False):
        admin_id_list.append(item.admin.pk)
    if int(admin_id) not in admin_id_list and admin_information.objects.filter(isDelete=False).get(pk=admin_id).level <100:
        return JsonResponse({
            'status': 'failure',
            'dis': "您不是此统计的管理员",
        })
    sta_inf.isDelete = True
    sta_inf.save()
    rec_inf = sta_inf.recond_set.all()
    for item in rec_inf:
        item.isDelete = True
        item.save()
    adm_sta_inf = sta_inf.admin_statistics_set.all()
    for item in adm_sta_inf:
        item.isDelete = True
        item.save()
    if os.path.exists(get_upload_dir()+str(sta_inf.pk)):
        shutil.rmtree(get_upload_dir()+str(sta_inf.pk))
    return JsonResponse({
        'status': 'success',
    })


def edit_sta_ajax(request):
    admin_id = request.COOKIES.get('admin_id')
    json_obj = request.POST.get('json')
    json_str = json.loads(json_obj)
    sta_id = json_str['sta']
    sta_inf = statistics_information.objects.filter(isDelete=False).get(pk=sta_id)
    admin_id_list = []
    for item in admin_statistics.objects.filter(statistics=sta_inf).filter(isDelete=False):
        admin_id_list.append(item.admin.pk)
    if int(admin_id) not in admin_id_list and admin_information.objects.filter(isDelete=False).get(pk=admin_id).level <100:
        return JsonResponse({
            'status': 'failure',
            'dis': '您不是此统计的管理员',
        })
    sta_inf.statistics_name = json_str['sta_name']
    sta_inf.statistics_description = json_str['description']
    if sta_inf.statistics_class != class_information.objects.filter(isDelete=False).get(pk=json_str["class_id"]):
        clear_sta(sta_inf.pk)
    if json_str['need_upload'] != sta_inf.need_upload:
        if json_str['need_upload']:
            os.mkdir(get_upload_dir() + str(sta_inf.pk))
            sta_inf.need_upload = True
        else:
            shutil.rmtree(get_upload_dir() + str(sta_inf.pk))
            sta_inf.need_upload = False
    sta_inf.save()
    admin_sta = admin_information.objects.filter(isDelete=False).all()
    admin_id = []
    for item in json_str['admin_id']:
        admin_id.append(int(item))
    for item in admin_sta:
        # print(item.admin)
        if item.pk in admin_id:
            try:
                obj = admin_statistics.objects.get(admin=item, statistics=sta_inf)
                obj.isDelete = False
            except admin_statistics.DoesNotExist:
                obj = admin_statistics()
                obj.admin = item
                obj.statistics = sta_inf
            obj.save()
        else:
            try:
                obj = admin_statistics.objects.get(admin=item, statistics=sta_inf)
                obj.isDelete = True
                obj.save()
            except admin_statistics.DoesNotExist:
                pass

    return JsonResponse({
        'status': 'success',
    })


def account_del_adm_ajax(request):
    adm_id = request.GET.get('adm_id')
    adm_inf = admin_information.objects.filter(isDelete=False).get(pk=adm_id)
    adm_inf.isDelete = True
    adm_inf.save()
    adm_sta_inf = adm_inf.admin_statistics_set.all()
    for item in adm_sta_inf:
        item.isDelete = True
        item.save()
    return JsonResponse({
        'status': 'success',
    })
