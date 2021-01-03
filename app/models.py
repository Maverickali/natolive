# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Injections(models.Model):
    record_id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=50)
    date = models.DateField()
    cash_forward = models.FloatField(default=0.0)
    repeat_customer_numbers = models.IntegerField(default=0)
    new_customer_numbers = models.IntegerField(default=0)
    repeat_customer_amount = models.FloatField(default=0.0)
    new_customer_amount = models.FloatField(default=0.0)
    cash_reserve_need = models.FloatField(default=0.0) 
    injection_amount = models.FloatField(default=0.0, null=True)
    injection_status = models.BooleanField(default=False)
    injection_authorization = models.CharField(max_length=10,default='False')
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50)
    update_date = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.CharField(max_length=50, null=True)

class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=50, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50)

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     branch_id = models.CharField(default=False, max_length=100)
#     location = models.CharField(default=False, max_length=100)
#     creationdate = models.DateField(default=False)