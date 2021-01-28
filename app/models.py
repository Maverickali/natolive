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
    updated_by = models.IntegerField(default=False, null=True)

class Branch(models.Model):
    id = models.AutoField(primary_key=True)
    branch_name = models.CharField(max_length=50, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    location = models.CharField(default=False, max_length=100)
    created_on = models.DateField(default=False)
    created_by = models.IntegerField(default=False)
    update_on = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.IntegerField(default=False, null=True)

class RM_Daily_Activity(models.Model):
    id = models.BigAutoField(primary_key=True)
    cilents_collected = models.IntegerField(default=0)
    amount_collected = models.FloatField(default=0.0, null=True)
    new_cilents = models.IntegerField(default=0)
    amount_disbursed = models.FloatField(default=0.0)
    activitydate = models.DateField(default=False)
    before_authorization = models.CharField(default=False, max_length=23)
    after_authorization = models.CharField(default=False, max_length=23)
    authorization_note = models.CharField(default='Not Authorized By Branch Manager', max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=False)
    update_on = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.IntegerField(default=False, null=True)

class RM_Weekly_Customers_Portfolio(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_date = models.DateField(default=False)
    to_date = models.DateField(default=False)
    day_category = models.CharField(default=False, max_length=50)
    portfolio_clients = models.IntegerField(default=0)
    portfolio_amount = models.FloatField(default=0.0)
    before_authorization = models.CharField(default=False, max_length=23, null=True)
    after_authorization = models.CharField(default=False, max_length=23, null=True)
    authorization_note = models.CharField(default='Not Authorized By Branch Manager', max_length=100, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=False)
    update_on = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.IntegerField(default=False, null=True)

class RM_Weekly_Customers(models.Model):
    id = models.BigAutoField(primary_key=True)
    from_date = models.DateField(default=False)
    to_date = models.DateField(default=False)
    customer_category = models.CharField(default=False, max_length=50)
    number_customers = models.IntegerField(default=0)
    before_authorization = models.CharField(default=False, max_length=23, null=True)
    after_authorization = models.CharField(default=False, max_length=23, null=True)
    authorization_note = models.CharField(default='Not Authorized By Branch Manager', max_length=100, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=False)
    update_on = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.IntegerField(default=False, null=True)


class Targets_Collections_Disbursement(models.Model):
    id = models.BigAutoField(primary_key=True)
    collections = models.FloatField(default=0.0)
    disbursements = models.FloatField(default=0.0)
    new_customers = models.FloatField(default=0.0)
    rm_id = models.IntegerField(default=False)
    active_portfoilo = models.FloatField(default=0.0)
    bad_portfoilo = models.FloatField(default=0.0)
    from_date = models.DateField(default=False)
    to_date = models.DateField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=False)
    update_on = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.IntegerField(default=False, null=True)


class Targets_Portfoilo(models.Model):
    id = models.BigAutoField(primary_key=True)
    rm_id = models.IntegerField(default=False)
    active_portfoilo = models.FloatField(default=0.0)
    bad_portfoilo = models.FloatField(default=0.0)
    from_date = models.DateField(default=False)
    to_date = models.DateField(default=False)
    day_category = models.CharField(default=False, max_length=50)
    number_cilents = models.IntegerField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=False)
    update_on = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.IntegerField(default=False, null=True)

