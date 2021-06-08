from id_manager import views
from django.urls import path, include 

urlpatterns = [    
    path('manager/add_ID_details.html', views.add_id, name='add_id'),    
    path('manager/view_IDs.html', views.view_ids, name='view_ids'), 
    path('manager/id_request/<int:id>', views.id_request, name='id_request'),
    path('manager/id_receviced/<int:id>', views.id_receviced, name='id_receviced'),
    path('id_manager/withdrawn/<int:id>', views.withdrawn, name='withdrawn'),
    path('id_manager/receviced/<int:id>', views.receviced_id_manager, name='receviced'),
    path('manager/over_ride_reason', views.over_ride_reason, name="over_ride_reason")   
    
]