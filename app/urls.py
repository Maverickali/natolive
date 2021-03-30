from django.contrib import admin
from django.urls import path, re_path
from app import views, rm_views, manager_views

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('treasury/create.html', views.treasury_create, name='add_treasury'),
    path('treasury/view.html', views.treasury_report, name='view_treasury'),
    path('treasury/view/approved/<int:id>', views.approved_injection, name='approved_injection'),
    path('treasury/view/rejected/<int:id>', views.rejected_injection, name='rejected_injection'),
    path('treasury/view/view_assessment/<int:id>/<int:cash>', views.view_assessment, name='view_assessment'),
    
    # Rm Views
    path('rm/c_collection_sheet.html', views.rm_collection_sheet, name='rm_collection_sheet'),
    path('rm/potential_customer.html', views.potential_customer, name='potentialCustomer'),
    
    # # old urls need to be removed if they are not working
    # path('rm/view_daily_activity.html', views.rm_daily_view, name='rmDailyView'),
    # path('rm/create_weekly_assessments.html', views.rm_weekly_assessments_create, name='rmWeeklyAssessmentCreate'),
    # path('rm/view_weekly_assessments.html', views.rm_weekly_assessments_view, name='rmWeeklyAssessmentView'),

    # # Manager Views
    # path('manager/set_targets.html', views.set_targets, name='setTargets'),
    # path('manager/view_set_targets.html', views.set_targets_view, name='setTargetsView'),
    path('manager/rm_collections.html', views.rm_collections, name='rm_collections'),  
    path('manager/rm_collections.html', views.post_authorization, name='post_authorization'),
      
    path('manager/add_disbursement.html', views.add_disbursement, name='add_disbursement'),    
    path('manager/view_disbursement.html', views.view_disbursement, name='view_disbursement'),   
    
    path('manager/add_daily_report.html', views.add_daily_report, name='addDailyReport'),
    path('manager/manage_rm.html', views.manage_rm, name='manage_rm')
    
# 
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
]
