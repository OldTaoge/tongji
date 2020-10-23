# File:ajax.py
# Copyright(C) OldTaoge 2020.All rights reserved.
# By GPL v3.0
import hashlib
import json
import os
import shutil
import time

from django.http import JsonResponse
from django.utils import timezone as d_tz
from pytz import timezone

from tongji.settings import get_upload_dir
from ..models import *


def query_description_by_statistics(statistics, stu_id):
    sta = statistics_information.objects.filter(isDelete=False).get(pk=statistics)
    description = sta.statistics_description
    stu_all = sta.statistics_class.student_information_set.filter().all()
    if os.path.exists(get_upload_dir() + str(statistics) + '/' + '0' + '/'):
        file_path = get_upload_dir() + str(statistics) + '/' + '0' + '/'
        description = add_tail(description, "<div class='carousel slide' id='carousel-0'>")
        description = add_tail(description, '<ol class="carousel-indicators">')
        file_num = len(os.listdir(file_path))
        description = add_tail(description, '<li class="active" data-slide-to="0" data-target="#carousel-0"></li>')
        for file_p in range(1, file_num):
            description = add_tail(description, '<li data-slide-to="' + str(file_p) + '" data-target="#carousel-0"></li>')
        description = add_tail(description, '</ol>')
        description = add_tail(description, '<div class="carousel-inner">')
        description = add_tail(description, '<div class="item active"><img alt="" src="/static/upload/'+str(statistics)+'/'+'0'+'/'+os.listdir(file_path)[0]+'" /></div>')
        for file_src in os.listdir(file_path)[1:]:
            description = add_tail(description, '<div class="item"><img alt="" src="/static/upload/'+str(statistics)+'/'+'0'+'/'+file_src+'" /></div>')
        description = add_tail(description, "</div>")
        description = add_tail(description, '<a class="left carousel-control" href="#carousel-0" data-slide="prev"><span class="glyphicon glyphicon-chevron-left"></span></a>')
        description = add_tail(description,'<a class="right carousel-control" href="#carousel-0" data-slide="next"><span class="glyphicon glyphicon-chevron-right"></span></a>')
        description = add_tail(description, "</tr></td>")
        description = add_tail(description, "</div>")
    stu_id_all =[]
    for item in stu_all:
        stu_id_all.append(int(item.pk))
    params = hashlib.md5((str(statistics)+str(round((time.time())*1000000))+str(stu_id)).encode(encoding='UTF-8')).hexdigest()
    if int(stu_id) in stu_id_all:
        # print(statistics, stu_id, stu_id_all)
        add_recond(statistics, stu_id, setread=1)
        if recond.objects.filter(isDelete=False).get(statistics=sta, stu_id=stu_id).reconded:
            stat = {
                'description': description,
                'need_upload': sta.need_upload,
                'params': params,
                'status': '已提交',
            }
        else:
            stat = {
                'description': description,
                'need_upload': sta.need_upload,
                'params': params,
                'status': '未提交',
            }
    else:
        stat = {
            'description': description,
            'need_upload': sta.need_upload,
            'params': params,
            'status': '',
        }
    return JsonResponse(stat)


def add_recond(statistics, stu_id, file_params='', setread=0):
    is_exists = recond.objects.all().filter(isDelete=False).filter(statistics=statistics_information.objects.get(pk=statistics)).filter(stu_id=stu_id).exists()  # 查重
    if setread == 1:
        if not is_exists:
            recond_inf = recond()
            recond_inf.statistics = statistics_information.objects.get(pk=statistics)
            recond_inf.student = student_information.objects.filter(isDelete=False).get(pk=stu_id)
            recond_inf.stu_id = int(stu_id)
            recond_inf.add_dt = d_tz.now()
            recond_inf.readed = True
            recond_inf.reconded = False
            recond_inf.inf = 'null'
            recond_inf.url = 'null'
        else:
            # print("********")
            recond_inf = recond.objects.filter(isDelete=False).get(statistics=statistics_information.objects.get(pk=statistics), stu_id=stu_id)
            recond_inf.statistics = statistics_information.objects.filter(isDelete=False).get(pk=statistics)
            recond_inf.student = student_information.objects.filter(isDelete=False).get(pk=stu_id)
            recond_inf.stu_id = int(stu_id)
            recond_inf.add_dt = d_tz.now()
            recond_inf.readed = True
            recond_inf.inf = 'null'
            recond_inf.url = 'null'
        recond_inf.save()
    else:
        if file_params != '':
            file_tmp_dir = get_upload_dir() + file_params
            file_new_dir = get_upload_dir() + str(statistics) + '/' + str(student_information.objects.filter(isDelete=False).get(pk=stu_id).pk)
            try:
                os.mkdir(file_new_dir)
            except FileExistsError:
                pass
            else:
                pass
            try:
                for file_name in os.listdir(file_tmp_dir):
                    shutil.copyfile(file_tmp_dir + '/' + file_name, file_new_dir + '/' + file_name)
                shutil.rmtree(file_tmp_dir)
            except FileNotFoundError:
                pass
            else:
                pass
            # print(file_tmp_dir)
            # print(file_new_dir)
        if not is_exists:
            recond_inf = recond()
            recond_inf.statistics = statistics_information.objects.get(pk=statistics)
            recond_inf.student = student_information.objects.filter(isDelete=False).get(pk=stu_id)
            recond_inf.stu_id = int(stu_id)
            recond_inf.add_dt = d_tz.now()
            recond_inf.readed = True
            recond_inf.reconded = True
            recond_inf.inf = 'null'
            recond_inf.url = 'null'
        else:
            # print("********")
            recond_inf = recond.objects.filter(isDelete=False).get(statistics=statistics_information.objects.get(pk=statistics), stu_id=stu_id)
            recond_inf.statistics = statistics_information.objects.filter(isDelete=False).get(pk=statistics)
            recond_inf.student = student_information.objects.filter(isDelete=False).get(pk=stu_id)
            recond_inf.stu_id = int(stu_id)
            recond_inf.add_dt = d_tz.now()
            recond_inf.readed = True
            recond_inf.reconded = True
            recond_inf.inf = 'null'
            recond_inf.url = 'null'
        recond_inf.save()
    stat = {
        'status': 'success',
    }
    return JsonResponse(stat)


def get_result_by_sta(statistics, ua):
    sta = statistics_information.objects.filter(isDelete=False).get(pk=statistics)
    reconds = sta.recond_set.all().filter(isDelete=False).filter(reconded=True).order_by('stu_id')
    stu_inf_all = sta.statistics_class.student_information_set.all()
    stu_statistical = {}
    stu_unstatistical = {}
    stu_reconded = []
    l_sta = 0
    l_unsta = 0
    for item in reconds:
        l_sta = l_sta + 1
        stu_reconded.append(item.stu_id)
        if sta.need_upload and os.path.exists(get_upload_dir()+str(item.statistics.pk)+'/'+str(item.stu_id)):
            try:
                stu_statistical[l_sta] = "<tr><td>" + student_information.objects.filter(isDelete=False).get(pk=item.stu_id).student_name + ' ' + str(item.add_dt.astimezone(timezone('Asia/Shanghai')))[:19]
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], "<div class='carousel slide' id='carousel-" + str(l_sta) + "'>")
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<ol class="carousel-indicators">')
                file_num = len(os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id)))
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<li class="active" data-slide-to="0" data-target="#carousel-' + str(l_sta) + '"></li>')
                for file_p in range(1, file_num):
                    stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<li data-slide-to="' + str(file_p) + '" data-target="#carousel-' + str(l_sta) + '"></li>')
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '</ol>')
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="carousel-inner">')
                if ua == 'weixin':
                    file_src = os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]
                    if file_src.split(".")[-1].lower() == "jpg" or file_src.split(".")[-1].lower() == "png":
                        stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item active"><img alt="" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'" /></div>')
                    if os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "mp4" or os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "mov":
                        stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item active"><video class="container" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'" ></video></div>')
                    for file_src in os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[1:]:
                        if file_src.split(".")[1].lower() == "jpg" or file_src.split(".")[-1].lower() == "png":
                            stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item"><img alt="" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'" /></div>')
                        if file_src.split(".")[1].lower() == "mp4" or file_src.split(".")[-1].lower() == "mov":
                            stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item"><video class="container" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'" ></video></div>')
                else:
                    file_src = os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]
                    if file_src.split(".")[-1].lower() == "jpg" or file_src.split(".")[-1].lower() == "png":
                        stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item active"><a target="_blank" href="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'"><img alt="" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'" /></a></div>')
                    if os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "mp4" or os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "mov":
                        stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item active"><a target="_blank" href="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'"><video class="container" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'"></video></a></div>')
                    for file_src in os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[1:]:
                        if file_src.split(".")[-1].lower() == "jpg" or file_src.split(".")[-1].lower() == "png":
                            stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item"><a target="_blank" href="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'"><img alt="" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'" /></a></div>')
                        if file_src.split(".")[-1].lower() == "mp4" or file_src.split(".")[-1].lower() == "mov":
                            stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item"><a target="_blank" href="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'"><video  class="container" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'" /></a></div>')
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], "</div>")
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<a class="left carousel-control" href="#carousel-'+str(l_sta)+'" data-slide="prev"><span class="glyphicon glyphicon-chevron-left"></span></a>')
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta],'<a class="right carousel-control" href="#carousel-'+str(l_sta)+'" data-slide="next"><span class="glyphicon glyphicon-chevron-right"></span></a>')
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], "</tr></td>")
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], "</div>")
            except IndexError:
                pass
            else:
                pass
        else:
            stu_statistical[l_sta] = "<tr><td>" + student_information.objects.filter(isDelete=False).get(pk=item.stu_id).student_name + str(item.add_dt.astimezone(timezone('Asia/Shanghai')))[:19] + "</tr></td>"
        # print(stu_statistical[l_sta])
    for item in stu_inf_all:
        if item.pk not in stu_reconded:
            if sta.recond_set.all().filter(isDelete=False).filter(stu_id=item.pk).filter(readed=True).exists():
                l_unsta = l_unsta + 1
                stu_unstatistical[l_unsta] = "<tr><td>" + item.student_name + "<small>已读</small></tr></td>"
    for item in stu_inf_all:
        if item.pk not in stu_reconded:
            if not sta.recond_set.all().filter(isDelete=False).filter(stu_id=item.pk).filter(readed=True).exists():
                l_unsta = l_unsta + 1
                stu_unstatistical[l_unsta] = "<tr><td>" + item.student_name + "<small>未读</small></tr></td>"
    sent_dic = {
        'description': sta.statistics_description,
        'l_sta': l_sta,
        'l_unsta': l_unsta,
        'statistical': stu_statistical,
        'unstatistical': stu_unstatistical,
        'file_tag': sta.need_upload,
    }
    return JsonResponse(sent_dic)


def get_result_by_sta_where_stu_list(statistics, ua, stu_id_list):
    stu_id_list = json.loads(stu_id_list)
    sta = statistics_information.objects.filter(isDelete=False).get(pk=statistics)
    reconds = sta.recond_set.all().filter(isDelete=False).filter(reconded=True).order_by('stu_id')
    stu_inf_all = sta.statistics_class.student_information_set.all()
    stu_statistical = {}
    stu_unstatistical = {}
    stu_reconded = []
    l_sta = 0
    l_unsta = 0
    for item in reconds:
        if item.stu_id not in stu_id_list:
            continue
            pass
        l_sta = l_sta + 1
        stu_reconded.append(item.stu_id)
        if sta.need_upload and os.path.exists(get_upload_dir()+str(item.statistics.pk)+'/'+str(item.stu_id)):
            try:
                stu_statistical[l_sta] = "<tr><td>" + student_information.objects.filter(isDelete=False).get(pk=item.stu_id).student_name + ' ' + str(item.add_dt.astimezone(timezone('Asia/Shanghai')))[:19]
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], "<div class='carousel slide' id='carousel-" + str(l_sta) + "'>")
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<ol class="carousel-indicators">')
                file_num = len(os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id)))
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<li class="active" data-slide-to="0" data-target="#carousel-' + str(l_sta) + '"></li>')
                for file_p in range(1, file_num):
                    stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<li data-slide-to="' + str(file_p) + '" data-target="#carousel-' + str(l_sta) + '"></li>')
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '</ol>')
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="carousel-inner">')
                if ua == 'weixin':
                    if os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "jpg" or os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "png":
                        stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item active"><img alt="" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'" /></div>')
                    if os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "mp4" or os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "mov":
                        stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item active"><video class="container" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'" ></video></div>')
                    for file_src in os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[1:]:
                        if file_src.split(".")[-1].lower() == "jpg" or file_src.split(".")[1].lower() == "png":
                            stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item"><img alt="" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'" /></div>')
                        if file_src.split(".")[-1].lower() == "mp4" or file_src.split(".")[1].lower() == "mov":
                            stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item"><video class="container" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'" ></video></div>')
                else:
                    if os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "jpg" or os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "png":
                        stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item active"><a target="_blank" href="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'"><img alt="" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'" /></a></div>')
                    if os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "mp4" or os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0].split('.')[-1].lower() == "mov":
                        stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item active"><a target="_blank" href="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'"><video class="container" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[0]+'"></video></a></div>')
                    for file_src in os.listdir(get_upload_dir()+str(statistics)+'/'+str(item.stu_id))[1:]:
                        if file_src.split(".")[-1].lower() == "jpg" or file_src.split(".")[1].lower() == "jpg":
                            stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item"><a target="_blank" href="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'"><img alt="" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'" /></a></div>')
                        if file_src.split(".")[-1].lower() == "mp4" or file_src.split(".")[1].lower() == "mov":
                            stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<div class="item"><a target="_blank" href="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'"><video  class="container" src="/static/upload/'+str(statistics)+'/'+str(item.stu_id)+'/'+file_src+'" /></a></div>')
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], "</div>")
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], '<a class="left carousel-control" href="#carousel-'+str(l_sta)+'" data-slide="prev"><span class="glyphicon glyphicon-chevron-left"></span></a>')
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta],'<a class="right carousel-control" href="#carousel-'+str(l_sta)+'" data-slide="next"><span class="glyphicon glyphicon-chevron-right"></span></a>')
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], "</tr></td>")
                stu_statistical[l_sta] = add_tail(stu_statistical[l_sta], "</div>")
            except IndexError:
                pass
            else:
                pass
        else:
            stu_statistical[l_sta] = "<tr><td>" + student_information.objects.filter(isDelete=False).get(pk=item.stu_id).student_name + str(item.add_dt.astimezone(timezone('Asia/Shanghai')))[:19] + "</tr></td>"
        # print(stu_statistical[l_sta])
    for item in stu_inf_all:
        if item.pk not in stu_id_list:
            continue
            pass
        if item.pk not in stu_reconded:
            if sta.recond_set.all().filter(isDelete=False).filter(stu_id=item.pk).filter(readed=True).exists():
                l_unsta = l_unsta + 1
                stu_unstatistical[l_unsta] = "<tr><td>" + item.student_name + "<small>已读</small></tr></td>"
    for item in stu_inf_all:
        if item.pk not in stu_id_list:
            continue
            pass
        if item.pk not in stu_reconded:
            if not sta.recond_set.all().filter(isDelete=False).filter(stu_id=item.pk).filter(readed=True).exists():
                l_unsta = l_unsta + 1
                stu_unstatistical[l_unsta] = "<tr><td>" + item.student_name + "<small>未读</small></tr></td>"
    sent_dic = {
        'description': sta.statistics_description,
        'l_sta': l_sta,
        'l_unsta': l_unsta,
        'statistical': stu_statistical,
        'unstatistical': stu_unstatistical,
        'file_tag': sta.need_upload,
    }
    return JsonResponse(sent_dic)


def clear_sta(statistics):
    sta = statistics_information.objects.filter(isDelete=False).get(pk=statistics)
    reconds = sta.recond_set.all()
    for items in reconds:
        items.isDelete = True
        items.save()
    if sta.need_upload:
        file_dir = get_upload_dir()+str(statistics)
        for url in os.listdir(file_dir):
            shutil.rmtree(file_dir+'/'+url)
    return JsonResponse({'status': 'success'})


def add_description(json_str):
    json_str = json.loads(json_str)
    # json_str['description']
    file_params = json_str['file_params']
    file_tmp_dir = get_upload_dir() + file_params + '/'
    for item in json_str['statistics']:
        sta_inf = statistics_information.objects.filter(isDelete=False).get(pk=item)
        sta_inf.statistics_description = str(json_str['description']).replace('\n', '<br>')
        sta_inf.save()
        file_new_dir = get_upload_dir() + str(sta_inf.pk) + '/' + '0' + '/'
        if os.path.exists(file_tmp_dir):
            try:
                os.makedirs(file_new_dir)
            except FileExistsError:
                pass
            else:
                pass
            for file_name in os.listdir(file_new_dir):
                os.remove(file_new_dir + file_name)
            for file_name in os.listdir(file_tmp_dir):
                shutil.copyfile(file_tmp_dir + file_name, file_new_dir + file_name)
    shutil.rmtree(file_tmp_dir)
    return JsonResponse({'status': 'success'})


def check_login_token(token, admin_id):
    sta_inf = admin_information.objects.filter(isDelete=False).get(pk=admin_id)
    if token == sta_inf.token:
        return JsonResponse({
            'status': 'true',
        })
    else:
        return JsonResponse({
            'status': 'false',
        })


def add_tail(str, add_str):
    str = str + add_str
    return str
