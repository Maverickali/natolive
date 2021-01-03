# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from django.contrib import admin
from django.urls import path, re_path
from app import views

urlpatterns = [
    # The home page
    path('dashboard/', views.index, name='home'),
    path('treasury/create.html', views.treasury_create, name='treasuryCreate'),
    path('treasury/view.html', views.treasury_report, name='treasuryReport'),
    path('treasury/view/approved/<int:id>', views.approved_injection, name='approved_injection'),
    path('treasury/view/rejected/<int:id>', views.rejected_injection, name='rejected_injection') 
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
]
