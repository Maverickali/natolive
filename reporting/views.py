from django.shortcuts import render
from reporting.form import Daily_report_search
from app.models import Branch, Daily_Report
from app.functions import get_user_group
from django.db.models import Sum
import datetime
from clusters.models import Assignments, Cluster_branches, Clusters

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
    user_group = get_user_group(request)
    if 'Supervisor'  in user_group :
        cluster_id = Assignments.objects.get(user_id=request.user)        
        branches = Cluster_branches.objects.filter(cluster_id_id=cluster_id.cluster_id_id)
    else:
        branches =  Branch.objects.all()
        
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
        'branches': branches,  
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
    activity_data_test = None
    form = Daily_report_search()
    #activity_data = Daily_Report.objects.select_related('customer_id').filter().order_by('-created_on')
    # add checker for who can do this
    if request.method == 'POST' and request.POST:
        branch_id = request.POST.get('branch', False)
        to_date = request.POST.get('to_date', False)
        from_date = request.POST.get('from_date', False)        
        activity_data = Daily_Report.objects.filter(branch_id=branch_id, activity_date__range=(from_date, to_date))
        days =  datetime.datetime.strptime(to_date,'%Y-%m-%d') - datetime.datetime.strptime(from_date,'%Y-%m-%d')
        
        if not activity_data:
            msg="No Report Found "# + days
            msg_status=False
        else:
            msg="Report Found For Nato " + str(branch_id) + " From the Date :- " + str(from_date) + " To the Date " + str(to_date) 
            activity_data_test = activity_data.aggregate(
                opening_bal=Sum('opening_bal') / days.days, 
                total_collections=Sum('total_collections') / days.days,
                total_processing_fees=Sum('total_processing_fees') / days.days,
                total_disbursed=Sum('total_disbursed') / days.days,
                injection_in=Sum('injection_in') / days.days,
                injection_out=Sum('injection_out') / days.days,
                total_banked=Sum('total_banked') / days.days,
                total_expenses_daily=Sum('total_expenses_daily') / days.days,
                closing_bal=Sum('closing_bal') / days.days,
                previous_closing_portfolio=Sum('previous_closing_portfolio') / days.days,
                total_clients_disbursed=Sum('previous_closing_portfolio') / days.days
                )
            # appending elements to the diction
            activity_data_test['branch'] = branch_id
            
            
            msg_status=True
        
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        'customerddl': customers,  
        'activity_data_test':activity_data_test, 
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'reporting/avgdaily_report_arch.html', context)
    