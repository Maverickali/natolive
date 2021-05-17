from reporting import views
from django.urls import path, include 

urlpatterns = [    
    path('reporting/daily_report_arch.html', views.daily_report, name='daily_report'),    
    path('reporting/avgdaily_report_arch.html', views.avg_daily_report, name='avg_daily_report'), 
     
    
]