from django.shortcuts import render
from reporting.form import Daily_report_search
from app.models import Daily_Report
from app.functions import get_user_group
import datetime

# Create your views here.

def daily_report(request):
    form = None
    activity_data = None
    msg = None
    msg_status = None
    customers = None
    creator = None
    active = 'daily_report'
    form = Daily_report_search()
    #activity_data = Daily_Report.objects.select_related('customer_id').filter().order_by('-created_on')
    # add checker for who can do this
    if request.method == 'POST' and request.POST:
        branch_id = request.POST.get('branch', False)
        to_date = request.POST.get('to_date', False)
        from_date = request.POST.get('from_date', False)        
        activity_data = Daily_Report.objects.filter(branch_id=branch_id, activity_date__range=(from_date, to_date)).order_by('-created_on')
        if not activity_data:
            msg="Report Found"
            msg_status=True
        else:
            msg="No Report Found"
            msg_status=False
        
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        'customerddl': customers,  
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'reporting/daily_report_arch.html', context)

def avg_daily_report(request):
    form = None
    activity_data = None
    msg = None
    msg_status = None
    customers = None
    creator = None
    active = 'daily_report'
    form = Daily_report_search()
    #activity_data = Daily_Report.objects.select_related('customer_id').filter().order_by('-created_on')
    # add checker for who can do this
    if request.method == 'POST' and request.POST:
        branch_id = request.POST.get('branch', False)
        to_date = request.POST.get('to_date', False)
        from_date = request.POST.get('from_date', False)        
        activity_data = Daily_Report.objects.filter(branch_id=branch_id, activity_date__range=(from_date, to_date)).order_by('-created_on')
       # days =  datetime.datetime.strptime(to_date,).day - datetime.datetime.strptime(from_date).day
        if not activity_data:
            msg="Report Found "# + days
            msg_status=True
        else:
            msg="No Report Found " # + days
            msg_status=False
        
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        'customerddl': customers,  
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'reporting/avgdaily_report_arch.html', context)
    