from reporting import views
from django.urls import path, include 

urlpatterns = [    
    path('reporting/daily_report_arch.html', views.daily_report, name='daily_report'),    
    path('reporting/avgdaily_report_arch.html', views.avg_daily_report, name='avg_daily_report'),    
    path('reporting/collection_report.html', views.collection_report, name='collection_report'),
    path('reporting/customer_base_report.html', views.customer_base_report, name='customer_base_report'),
    path('reporting/daily_report_cluster.html', views.daily_report_cluster, name='daily_report_cluster'), 
    path('reporting/ids_report.html', views.ids_report, name='ids_report'),
    path('reporting/approve_reject_rm.html', views.approve_reject_rm, name='approve_reject_rm'),    
    path('reporting/rm_activate/<int:id>', views.rm_activate, name='activate'),
    path('reporting/rm_deactivate/<int:id>', views.rm_deactivate, name='deactivate')
    
    
    
    
     
    
]