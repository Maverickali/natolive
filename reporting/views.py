from django.shortcuts import render
from reporting.form import Daily_report_search
from app.models import Branch, Daily_Report, Potential_Customers, Profile, RM_Collection_Sheets
from app.functions import getSupaClustorBranches, get_user_group
from django.db.models import Sum
import datetime
from clusters.models import Assignments, Cluster_branches, Clusters
from id_manager.models import Ids
from django.contrib.auth.models import User

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
    
    
    
    
def collection_report(request):
    # Showing pending and approved collections
    # Get supervisor branches in cluster 
    active = None 
    msg = None
    msg_status = None 
    cluster_id = None
    active = 'supa_reports'
    cluster = Assignments.objects.select_related('user_id', 'cluster_branch_id', 'cluster_id').filter(user_id=request.user.id).values('cluster_branch_id_id__cluster_id' )
    for b in cluster:
        cluster_id = b
    cluster_instance = Clusters.objects.get(id=cluster_id['cluster_branch_id_id__cluster_id'])
    # Supervisor's cluster class
    branches = Cluster_branches.objects.filter(cluster_id=cluster_instance)
    branches_values = branches.values('branch_id')
    activity_data = RM_Collection_Sheets.objects.filter(branch_id__in=branches_values)
    if request.method == 'POST' and request.POST:
        branches = request.POST.getlist('branches[]')
        to_date = request.POST.get('to_date', False)
        from_date = request.POST.get('from_date', False)
        activity_data = RM_Collection_Sheets.objects.filter(branch_id__in=branches , collection_date__range=(from_date, to_date))
        if activity_data:
            msg="Collection Report From:- "+str(from_date)+" To:- "+str(to_date) +" For the Selected Branch(es) :- Nato ( "+str(branches)+" )"
            msg_status=True
        else:
            msg="No Report Found"
            msg_status=False
    context = {        
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        'branches': branches,
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'reporting/collection_report.html', context)
    

def customer_base_report(request):
    # Showing active and Potential Clients
    active = None 
    msg = None
    msg_status = None 
    cluster_id = None
    # Supervisor's cluster class
    branches = getSupaClustorBranches(request)
    branches_values = branches.values('branch_id')
    activity_data = Potential_Customers.objects.filter(branch_id__in=branches_values)
    if request.method == 'POST' and request.POST:
        branches = request.POST.getlist('branches[]')
        customer_type = request.POST.get('customer_type', False)
        to_date = request.POST.get('to_date', False)
        from_date = request.POST.get('from_date', False)
        if customer_type == 'all':
            activity_data = Potential_Customers.objects.filter(branch_id__in=branches , created_on__range=(from_date, to_date))
        else:
            activity_data = Potential_Customers.objects.filter(branch_id__in=branches, turn_over=customer_type, created_on__range=(from_date, to_date))
            
        if activity_data:
            msg="Customer Base Report From:- "+str(from_date)+" To:- "+str(to_date) +" For the Selected Branch(es) :- Nato ( "+str(branches)+" )"
            msg_status=True
        else:
            msg="No Report Found"
            msg_status=False
    active = 'supa_reports'   
    
        
    context = {        
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        'branches': branches,
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'reporting/customer_base_report.html', context)


def ids_report(request):
    form = None
    activity_data = None
    msg = None
    msg_status = None
    customers = None
    creator = None
    active = 'supa_reports' 
    branches = getSupaClustorBranches(request)
    branches_values = branches.values('branch_id')
    activity_data = Ids.objects.select_related('customer_id').filter(branch_id__in=branches).order_by('-created_on')
   
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg,    
        # 'txn_date': get_Open_Txn_date(request),
        'msg_status': msg_status,
        'active': active,
        'customerddl': customers,  
        "currentGroup":  get_user_group(request)
        }
    
    return render(request, 'reporting/ids_report.html', context)

def daily_report_cluster(request):
    # Showing Daily Report
    pass

def approve_reject_rm(request):
    activity_data = None
    msg = None
    msg_status = None
    customers = None
    creator = None
    active = 'approve_reject_rm' 
    branches = getSupaClustorBranches(request)
    branches_values = branches.values('branch_id')
    # print(branches_values)
    activity_data = Profile.objects.select_related('user').filter(branch_id__in=branches_values, user__groups__in=[5])
   
   
    context = {
        'activity_data': activity_data,
        'msg': msg,    
        # 'txn_date': get_Open_Txn_date(request),
        'msg_status': msg_status,
        'active': active,
        'customerddl': customers,  
        "currentGroup":  get_user_group(request)
        }
    
    return render(request, 'reporting/approve_reject_rm.html', context)

def rm_activate(request,id):    
    activity_data = None
    msg = None
    msg_status = None
    active = 'approve_reject_rm' 
    branches = getSupaClustorBranches(request)
    branches_values = branches.values('branch_id')
    # print(branches_values)
    activity_data = Profile.objects.select_related('user').filter(branch_id__in=branches_values, user__groups__in=[5])
   
    Profile.objects.filter(id=id).update(is_active=True, update_on = datetime.datetime.now() )
    msg='Rm has been successfully Activated'
    msg_status=True   
        
    context = {
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'reporting/approve_reject_rm.html', context)

def rm_deactivate(request,id):
    activity_data = None
    msg = None
    msg_status = None
    active = 'approve_reject_rm' 
    branches = getSupaClustorBranches(request)
    branches_values = branches.values('branch_id')
    # print(branches_values)
    activity_data = Profile.objects.select_related('user').filter(branch_id__in=branches_values, user__groups__in=[5])
   
    Profile.objects.filter(id=id).update(is_active=False, update_on = datetime.datetime.now() )
    msg='Rm has been successfully Deactivated'
    msg_status=True   
        
    context = {
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'reporting/approve_reject_rm.html', context)
    