from django.contrib import admin
from eod import views
from django.urls import path, re_path


urlpatterns = [    
    path('manager/eod.html', views.eod, name='eod'),
]