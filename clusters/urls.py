from django.contrib import admin
from clusters import views
from django.urls import path, re_path

urlpatterns = [    
   path('cluster/create_cluster.html', views.manage_cluster, name='manage_cluster'), 
   path('cluster/assign_branches_cluster.html', views.assign_branches_cluster, name='assign_branches_cluster'),   
   path('cluster/assign_supa_cluster.html', views.assign_supa_cluster, name='assign_supa_cluster'),
   path('cluster/view_cluster.html', views.view_cluster, name='view_cluster'),
   
]