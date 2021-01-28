# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from app.models import Branch, Profile
from django.contrib.auth.models import Permission


admin.site.register(Permission)
admin.site.register(Branch)
admin.site.register(Profile)

