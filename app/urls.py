from django.contrib import admin
from django.urls import path, re_path
from app import views

urlpatterns = [
    # The home page
    path('', views.index, name='home'),
    path('treasury/create.html', views.treasury_create, name='treasuryCreate'),
    path('treasury/view.html', views.treasury_report, name='treasuryReport'),
    path('treasury/view/approved/<int:id>', views.approved_injection, name='approved_injection'),
    path('treasury/view/rejected/<int:id>', views.rejected_injection, name='rejected_injection'),
    path('rm/create_daily_activity.html', views.rm_daily_create, name='rmDailyCreate'),
    path('rm/view_daily_activity.html', views.rm_daily_view, name='rmDailyView'),
    path('rm/create_weekly_assessments.html', views.rm_weekly_assessments_create, name='rmWeeklyAssessmentCreate'),
    path('rm/view_weekly_assessments.html', views.rm_weekly_assessments_view, name='rmWeeklyAssessmentView'),
    path('manager/set_targets.html', views.set_targets, name='setTargets'),
    path('manager/view_set_targets.html', views.set_targets_view, name='setTargetsView')
    
    # path('manager/view_set_targets.html', views.rm_daily_view, name='rmDailyView')
    
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
]
