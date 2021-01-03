# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch_id = models.CharField(default=False, max_length=100)
    location = models.CharField(default=False, max_length=100)
    creationdate = models.DateField(default=False)