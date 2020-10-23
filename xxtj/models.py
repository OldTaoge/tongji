# File:models.py
# Copyright(C) OldTaoge 2020.All rights reserved.
# By GPL v3.0
from django.db import models


# Create your models here.


class class_information(models.Model):
    person_num = models.IntegerField()
    name_dis = models.CharField(max_length=50)
    isDelete = models.BooleanField(default=False)


class student_information(models.Model):
    student_name = models.CharField(max_length=20)
    student_class = models.ForeignKey("class_information", on_delete=models.CASCADE)
    isDelete = models.BooleanField(default=False)


class statistics_information(models.Model):
    statistics_class = models.ForeignKey("class_information", on_delete=models.CASCADE)
    statistics_name = models.CharField(max_length=20, default='none')
    statistics_description = models.CharField(max_length=4096)
    need_upload = models.BooleanField(default=False)
    statistics_inf = models.TextField()
    isDelete = models.BooleanField(default=False)


class admin_information(models.Model):
    admin_username = models.CharField(max_length=50)
    admin_password = models.CharField(max_length=100)
    token = models.CharField(max_length=50)
    level = models.IntegerField()
    isDelete = models.BooleanField(default=False)


class admin_statistics(models.Model):
    admin = models.ForeignKey("admin_information", on_delete=models.CASCADE)
    statistics = models.ForeignKey("statistics_information", on_delete=models.CASCADE)
    isDelete = models.BooleanField(default=False)


class recond(models.Model):
    student = models.ForeignKey("student_information", on_delete=models.CASCADE)
    statistics = models.ForeignKey("statistics_information", on_delete=models.CASCADE)
    stu_id = models.IntegerField()
    inf = models.TextField()
    url = models.TextField()
    readed = models.BooleanField(default=False)
    reconded = models.BooleanField(default=False)
    add_dt = models.DateTimeField()
    isDelete = models.BooleanField(default=False)
