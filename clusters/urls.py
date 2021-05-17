from django.contrib import admin
from clusters import views
from django.urls import path, re_path

urlpatterns = [    
   path('cluster/create_cluster.html', views.manage_cluster, name='manage_cluster'),   
   path('cluster/view_cluster.html', views.view_cluster, name='view_cluster'),
   path('cluster/view_cluster.html', views.add_branch_cluster, name='add_branch_cluster')
   
]