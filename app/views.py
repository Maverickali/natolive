# -*- encoding: utf-8 -*-
"""
Copyright (c) 
"""
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.urls import reverse
from django.utils import timezone
from django.views import generic 
from django.db.models import Count, Q, Sum
from django.contrib.auth.models import Group, User
from app.forms import BranchForm, Collection_Sheet_Form, Potential_Customers_Form, RMWeeklyCustomersForm, RMWeeklyCustomersPortfolioForm, Repeat_Potential_Customer, RmDailyActivityForm, SearchForm, SetTargetsForm, TargetsPortfoiloForm, TreasuryForm

from eod.models import Eod
from .functions import get_Open_Txn_date, branch_disable, get_date, getTotalClientsDisbursed, getTotalCollections, getTotalDisbursement
from app.models import Branch, Daily_Report, Disbursements, Injections, Potential_Customers, Profile, RM_Collection_Sheets, RM_Daily_Activity
import datetime
from datetime import date, timedelta
import re
from django.db import DatabaseError
from app.functions import mail, get_branch_id, get_desire_date, get_user_group
from app.manager_forms import Daily_Report_Form, Disbursement_Form, Disbursement_Search_Form, RM_Search_Collections_Form
from authentication.forms import SignUpForm
from django.core.exceptions import ObjectDoesNotExist
from clusters.models import Assignments, Cluster_branches



@login_required(login_url="/login/")
def index(request): 
    cash_forward = Injections.objects.aggregate(Sum('cash_forward'))  
    injection_amount = Injections.objects.aggregate(Sum('injection_amount'))  
    repeat_cust =  Injections.objects.aggregate(Sum('repeat_customer_numbers'))
    new_cust = Injections.objects.aggregate(Sum('new_customer_numbers'))
    potential_customers = Potential_Customers.objects.filter(turn_over='active_cilent').count()#.aggregate(sum('id'))
    active_customers = Potential_Customers.objects.filter(turn_over='potential_cilent').count()
    Injection_requests = Injections.objects.filter(injection_status=1).count()
    txn_date = get_Open_Txn_date(request) 
    # m = mail(request,"TEST MAIL", "This is a test mail", ["collinsmaverick11@gmail.com"])
    # if m == 1:
    #     print('sent')
    # else:
    #     print('not sent')
    context = {
        'active': 'home',
        'cash_forward': cash_forward['cash_forward__sum'],
        'repeat_cust': repeat_cust['repeat_customer_numbers__sum'],
        'new_cust': new_cust['new_customer_numbers__sum'],
        'injection_amount': injection_amount['injection_amount__sum'],
        'Injection_requests': Injection_requests,
        'active_customers': active_customers,
        'potential_customers': potential_customers,
        'txn_date': txn_date,
        "currentGroup": get_user_group(request)
        }

    return render(request, 'index.html', context)

def create_branch(request):    
    
    msg = None
    obj = None
    success = False
    form = BranchForm()
    active = 'treasury'
    activity_data = Branch.objects.all()
    if request.method == 'POST' and request.POST:
        form = BranchForm(request.POST)    
        if form.is_valid(): 
            createBranch = Branch.objects.get_or_create(branch_name=form.cleaned_data.get("branch_name"));
            if createBranch:
                last_id = Branch.objects.latest('id')
                
                # start eod
                initialEod = eod.objects.get_or_create(
                    branch_id=last_id,
                    transaction_date=datetime.date.today() )
                msg = initialEod
            else:
                msg = "Branch already exists"
            
        
    context = {
        'form': form, 
        'activity_data':activity_data,
        "msg": msg, 
        "success": success, 
        "obj" : obj,
        "currentGroup": get_user_group(request), 
        'active':active}

    return render(request, 'co-admin/create_branch.html', context)

def view_branch(request):
    pass

@login_required(login_url="/login/")
def treasury_create(request):
    msg     = None
    branch = None
    success = False
    current_user_groups = request.user.groups.values_list("name", flat=True)    
    if request.method == 'POST' and request.POST:
        branch_name = get_branch_id(request)      
        form = TreasuryForm(request.POST)    
        if form.is_valid(): 
            obj = form.save(commit=False)
            obj.branch_name = branch_name
            obj.created_by = request.user.id
            obj.cash_reserve_need = float(request.POST['cash_forward']) - (float(request.POST['new_customer_amount']) + float(request.POST['repeat_customer_amount']))
            obj.save()
            success = True 
            msg = 'Treasury Report Successfully Saved'
            msg_status = True
        else:
            msg = form.errors # msg= 'FORM IS INVALID'
            msg_status = False
    else:
        msg = 'No'
        form = TreasuryForm()
    # user_name = request.user.username                
    # form = branch_disable(user_name,'treasury')
    active = 'treasury'
    context = {
        'form': form, 
        'branch':branch,
        "msg": msg, 
        "success": success,  'txn_date' : get_Open_Txn_date(request),
        "currentGroup": get_user_group(request), 
        'active':active}

    return render(request, 'treasury/create.html', context)

def treasury_report(request):
    treasury_list = None
    msg = ''
    updated = None
    inj_status = None
    user_group = get_user_group(request)
    if 'Supervisor'  in user_group:
        cluster_id = Assignments.objects.get(user_id=request.user)        
        branches = Cluster_branches.objects.filter(cluster_id_id=cluster_id.cluster_id_id)
    elif 'Branch-Managers'  in user_group:
        branches =  Branch.objects.filter(id=get_branch_id(request))
    else:
        branches =  Branch.objects.all()
    if request.method == 'POST' and request.POST:
        search_form = SearchForm(request.POST)       
        if search_form.is_valid():            
            branch_id = request.POST.get('branch_name', False)
            inj_status = request.POST.get('inj_status', False)
            all_branchs = request.POST.get('all_branchs', False)
            to_d_year = int(request.POST['to_date_year'])
            to_d_month = int(request.POST['to_date_month'])
            to_d_day = int(request.POST['to_date_day'])
            from_d_year = int(request.POST['from_date_year'])
            from_d_month = int(request.POST['from_date_month'])
            from_d_day = int(request.POST['from_date_day'])
            to_date = datetime.date(to_d_year, to_d_month, to_d_day)
            from_date = datetime.date(from_d_year, from_d_month, from_d_day)            
            Total_expenses = ""
            Total_collections = getTotalCollections(request)
            Drawer_limit = ""
            Assessment = ""
            
           
            if inj_status == 'on':
                inj_status = 1
            else:
                inj_status = 0

            if all_branchs == 'on':
                treasury_list = Injections.objects.filter(
                    #injection_status=inj_status, 
                    date__range=(from_date, to_date)).order_by('-date')  
            elif all_branchs == 'on' and  inj_status == 'on':
                treasury_list = Injections.objects.filter(
                    injection_status=inj_status, 
                    date__range=(from_date, to_date)).order_by('-date')             
            else:
                all_branchs = False           
                treasury_list = Injections.objects.filter(
                    injection_status=inj_status, 
                    date__range=(from_date, to_date), 
                    branch_name=branch_id).order_by('-date')              
                
            search_form = SearchForm().full_clean()
        else:
            updated = False
            msg = "VALIDATION FAILED"
    else:
        search_form = SearchForm()
        treasury_list = Injections.objects.filter(
            injection_status=True,
            date=datetime.datetime.today()).order_by('-date')
 
    # msg = inj_status#Injections.objects.aggregate(Sum('cash_forward'))
    branch_name = Branch.objects.all()
    user_name = request.user.username    
    search_form = SearchForm()# branch_disable(user_name,'search')
    
    active = 'treasury'
    context = { 
            'treasuryList': treasury_list, 'searchform': search_form,
            # 'Branch': branch_name,
            'updated': updated,  'txn_date' : '',
            'msg': msg, "currentGroup": get_user_group(request),
            'branches':branches,
            'active':active}

    return render(request, 'treasury/view.html', context)

def view_assessment(request,id,cash):
    treasury_list = None
    treasury_list = Injections.objects.filter(injection_status=True,date=datetime.datetime.today()).order_by('-date') 
    updating = None
    msg = None
    collections = RM_Collection_Sheets.objects.filter(authorization_status='APPROVED', branch_id=id).aggregate(Sum('amount_collected'))
    Total_expenses = Daily_Report.objects.filter(branch_id=id).aggregate(Sum('total_expenses_daily'))
    Drawer_limit = 0.6  * int(Total_expenses['total_expenses_daily__sum'])  
    disbursement = Disbursements.objects.filter(branch_id=id).aggregate(Sum('amount_disbursed'))
    cash_forward =  Injections.objects.get(record_id=id)#filter(record_id=cash).order_by('-date')
    Assessment = ""
    # injectionin  = (total_disbursement + expenses) > (total collections+cash_forward)
    # injectionout = (total_disbursement + expenses) < (total collections+cash_forward)
    # banker = injectionout 
    if (int(disbursement['amount_disbursed__sum']) + int(Total_expenses['total_expenses_daily__sum'])) > (int(collections['amount_collected__sum']) + int(cash_forward.cash_forward)):
       Assessment = "injection In" 
    elif (int(disbursement['amount_disbursed__sum']) + int(Total_expenses['total_expenses_daily__sum'])) < (int(collections['amount_collected__sum']) + int(cash_forward.cash_forward)):
       Assessment = "injection Out" 
    else:
        Assessment = "Bank"
    context = { 
        'collections' : collections['amount_collected__sum'], 
        'expenses': Total_expenses['total_expenses_daily__sum'],
        'disbursement': disbursement['amount_disbursed__sum'], 
        'drawer' : Drawer_limit,
        'id': cash_forward.cash_forward,
        'record_id' : cash,
        'action': Assessment,
        'msg': msg, "currentGroup": get_user_group(request)}
    return render(request, 'accountant/view_assessment.html', context)
    
    
def approved_injection(request):
    treasury_list = None
    treasury_list = Injections.objects.filter(injection_status=True,date=datetime.datetime.today()).order_by('-date') 
    updating = None
    msg = None
    id = request.POST['id']
    comment = request.POST['comment']
    
    if request.user.has_perm('app.can_approve_reject_injection'):     
        # Injections.objects.all()   
        updated = Injections.objects.select_related().get(record_id=id)
        # treasury_list = updated
        updated.injection_authorization = 'APPROVED'
        updated.comment = comment
        updated.injection_status = False
        updated.updated_by = request.user.id
        if comment == '':
            updated = False  
            msg = 'Please Add a Comment to complete this action successfully'
        else:
            updated.save()
            updated = True  
            msg = 'Injection Approved Successfully'        
    else:
        return render(request, 'includes/noauthorization.html')
    search_form = SearchForm()
    context = { 
        'treasuryList' : treasury_list, 
        'searchform': search_form,
        'updated': updated,  'txn_date' : 'null',# get_Open_Txn_date(request),
        'msg': msg, "currentGroup": get_user_group(request)}
    return render(request, 'treasury/view.html', context)

def rejected_injection(request, id):
    treasury_list = None
    id = request.POST['id']
    comment = request.POST['comment']
    try:
        msg = None
        success = None
        if request.user.has_perm('app.can_approve_reject_injection'):     
            treasury_list = Injections.objects.filter(injection_status=True,date=datetime.datetime.today()).order_by('-date')
            updated = Injections.objects.select_related().get(record_id=id)
            updated.injection_authorization = 'REJECTED'
            updated.comment = comment
            updated.injection_status = False
            updated.updated_by = request.user.id
            if comment == '':
                updated = False  
                msg = 'Please Add a Comment to complete this action successfully'
            else:
                updated.save()
                updated = True  
                msg = 'Injection Rejected Successfully'
        else:
            return render(request, 'includes/noauthorization.html')
    except:
        success = "danger"
        msg = "Something Went Wrong DB LEVEL"
    search_form = SearchForm()
    context = { 
        'treasuryList' : treasury_list, 
        'searchform': search_form,
        'updated': updated,  'txn_date' : 'null',#get_Open_Txn_date(request),
        'msg': msg  }
    return render(request, 'treasury/view.html', context)

def approve_or_reject_injection(request):
    if request.POST and request.method == 'POST':
        if request.POST['approve'] == 'yes':
            approved_injection(request)
        else:
            rejected_injection(request)
    pass

def rm_daily_create(request):
    msg     = None
    success = False
    activity = None
    current_user_groups = request.user.groups.values_list("name", flat=True)
    if request.method == 'POST' and request.POST:
        form = RmDailyActivityForm(request.POST)
        if form.is_valid():           
            activitydate_year = int(request.POST['activitydate_year'])
            activitydate_month = int(request.POST['activitydate_month'])
            activitydate_day = int(request.POST['activitydate_day'])
            # Check if RM has save a daily activity yet using
            # activitydate and RM id
            activitydate = datetime.date(activitydate_year, activitydate_month, activitydate_day)
           
            try:
                selected_data = RM_Daily_Activity.objects.select_related().get(activitydate=activitydate)
            except RM_Daily_Activity.DoesNotExist: 
                selected_data = None
            if selected_data is None:
                obj = form.save(commit=False)
                obj.created_by = request.user.id
                obj.before_authorization = "PENDING"
                obj.save()
            else:
                selected_data.cilents_collected = request.POST['cilents_collected']
                selected_data.amount_collected = request.POST['amount_collected']
                selected_data.new_cilents = request.POST['new_cilents']
                selected_data.amount_disbursed = request.POST['amount_disbursed']
                selected_data.save()
                
            success = True 
            msg = 'SUCCESSFULLY SAVED'
        else:
            msg=form.errors
    else:
        form = RmDailyActivityForm()    
    current_date = datetime.date.today() 
    past_7_days = datetime.date.today() + timedelta(days=-7)
    activity = RM_Daily_Activity.objects.filter(activitydate__range=(past_7_days, current_date),created_by=request.user.id).order_by('-activitydate')
    context = {
        'form': form, 
        "msg": msg, 
        "success": success,
        "currentGroup": current_user_groups,
        "activity_data": activity}

    return render(request, 'rm/create_daily_activity.html', context)

def rm_daily_view(request):
    context = { "currentGroup": get_user_group(request)}
    return render(request, 'rm/view_daily_activity.html', context)

def rm_weekly_assessments_create(request):
    msg     = None
    success = False
    current_user_groups = request.user.groups.values_list("name", flat=True)
    if request.method == 'POST' and request.POST:
        if request.POST['actualCustomers'] == 'actualCustomers': 
            form = RMWeeklyCustomersForm(request.POST)
            if form.is_valid():                       
                obj = form.save(commit=False)
                obj.created_by = request.user.id
                obj.before_authorization = "PENDING"             
                obj.save()
                success = True 
                msg = 'SUCCESSFULLY SAVED'
            else:
                msg= form.errors
        else:
            form = RMWeeklyCustomersPortfolioForm(request.POST)
            if form.is_valid():                       
                obj = form.save(commit=False)
                obj.created_by = request.user.id
                obj.before_authorization = "PENDING"                
                obj.save()
                success = True 
                msg = 'SUCCESSFULLY SAVED'
            else:
                msg = form.errors

    else:
        msg='.'        
    
    form = RMWeeklyCustomersPortfolioForm()
    frm = RMWeeklyCustomersForm()       

    context = {
        'form': form, 
        'frm': frm, 
        "msg": msg, 
        "success": success,
         "currentGroup": get_user_group(request)}

    return render(request, 'rm/create_weekly_assessments.html', context)

def rm_weekly_assessments_view(request):
    pass
@login_required(login_url="/login/")
def set_targets(request):
    msg = None
    user = User.objects.all()  
    # profile = Profile.objects.all()# Profile.objects.select_related('user').filter(branch_id=get_branch_id(request), user__groups=5) 
    # rms = Profile.objects.select_related('user').filter(branch_id=get_branch_id(request), user__groups=5)  
    # Geting the branch id from the profile list
    # id = request.user.profile.branch_id_id
    # profile = Profile.objects.filter(branch_id_id=id)
    print(request.method)
    if request.method == 'POST' and request.POST:

        to_d_year = int(request.POST['to_date_year'])
        to_d_month = int(request.POST['to_date_month'])
        to_d_day = int(request.POST['to_date_day'])
        from_d_year = int(request.POST['from_date_year'])
        from_d_month = int(request.POST['from_date_month'])
        from_d_day = int(request.POST['from_date_day'])

        to_date = datetime.date(to_d_year, to_d_month, to_d_day)
        from_date = datetime.date(from_d_year, from_d_month, from_d_day)

        days = to_date.day - from_date.day 
        
        if request.POST['frmcollections'] == 'form1':
            form = SetTargetsForm(request.POST)
        else:
            form = TargetsPortfoiloForm(request.POST)

        if form.is_valid():
            if days == 6:            
                obj = form.save(commit=False)
                obj.created_by = request.user.id
                # obj.before_authorization = "PENDING-APPROVAL"
                # obj.after_authorization = ""
                # obj.authorization_note = ""
                # obj.cash_reserve_need = float(request.POST['cash_forward']) - (float(request.POST['new_customer_amount']) + float(request.POST['repeat_customer_amount']))
                obj.save()
                success = True 
                msg = 'SUCCESSFULLY SAVED'
            else:
                msg = ''
        else:
            msg= form.errors

    form = SetTargetsForm()
    portfolioForm = TargetsPortfoiloForm()
    context = {
        'form': form, 
        'frmportfoilo': portfolioForm, 
        'msg': msg, 
        #  'ddlrms': rms,
        #  'profile': profile,
         'user' : user}
    return render(request, 'manager/set_targets.html', context)

def set_targets_view(request):
    pass


# START RM Views 
def rm_collection_sheet(request):
    
    
    # Post 
    
    msg = None
    msg_status = None
    success = None
    receipt_no = None
    active = None
    customers = None
    activity_data = None
    try:
        last_id = RM_Collection_Sheets.objects.latest('id')        
    except ObjectDoesNotExist:
        last_id = 0
    try:
        activity_data = RM_Collection_Sheets.objects.select_related('customer').filter(created_by=request.user.id)         
    except ObjectDoesNotExist:
        activity_data = None
    try:
        customers =  Potential_Customers.objects.filter(reassigned_to=request.user.id, branch_id=get_branch_id(request) , turn_over='active_cilent' ).order_by('-created_on')  | Potential_Customers.objects.filter( branch_id=get_branch_id(request) , turn_over='active_cilent', created_by=request.user.id ).order_by('-created_on')    | Potential_Customers.objects.filter( branch_id=get_branch_id(request) , turn_over='active_cilent' ).order_by('-created_on')   
    except ObjectDoesNotExist:
        customers = None
    
    if request.method == 'POST' and request.POST:
        if last_id == 0:
            receipt_no =  str(request.user.id) + str(get_branch_id(request)) + '0'
        else :
            receipt_no = str(request.user.id) + str(get_branch_id(request)) + str(last_id.id)
        form = Collection_Sheet_Form(request.POST)        
        if form.is_valid():
            collection_date = get_Open_Txn_date(request)
            customer_id = request.POST.get('customer_id',False)
            customer_instance = Potential_Customers.objects.get(id=customer_id)
            # receipt_no = request.POST['receipt_number']
            creator = request.user.id
            checker = None
            try:
                # Go to db
                checker = RM_Collection_Sheets.objects.filter(receipt_number=receipt_no)
                if not checker :                    
                    obj = form.save(commit=False)
                    obj.receipt_number = receipt_no
                    # put rm reponsible for collection 
                    obj.created_by = creator
                    obj.customer = customer_instance
                    obj.branch_id = get_branch_id(request)
                    obj.before_authorization = "PENDING"
                    obj.collection_date = collection_date
                    obj.collected_by = request.user.id
                    obj.save()
                    msg_status = True
                    msg = 'COLLECTION WAS SUCCESSFULLY SAVED WITH RECEIPT NUMBER:- ' + str(receipt_no)
                    form = Collection_Sheet_Form().full_clean()
                    form = Collection_Sheet_Form()
                    # last_id = RM_Collection_Sheets.objects.latest('id')
                    # receipt_no = str(request.user.id) + str(get_branch_id(request)) + str(last_id.id)     
                    
                else:
                    msg = "You have Already Used this Receipt number CAN'T SAVE THIS COLLECTION"
                    msg_status = False

            except DatabaseError as e:
                msg = e  
                msg_status = False             
        else:
            msg = form.errors
            msg_status = False
    else:
        form = Collection_Sheet_Form()
        
    active = 'collections_sheet'
    context = {
        'form': form,
        'msg_status': msg_status,
        'activity_data': activity_data,
        'receipt_no' : receipt_no,
        'msg': msg, 
        'customerddl': customers,
        'txn_date' : get_Open_Txn_date(request),
        'active': active,
        "currentGroup": get_user_group(request)
    }

    return render(request, 'rm/c_collection_sheet.html', context)

def potential_customer(request):
    activity_data = None
    active = None
    msg = None
    form = None 
    msg_status = None
    creator = request.user.id
    form = Potential_Customers_Form()
    activity_data = Potential_Customers.objects.filter(created_by=creator)    
    if request.method == 'POST' and request.POST:
        form = Potential_Customers_Form(request.POST)
        desire_date = get_desire_date(request)
        if form.is_valid():
            # ADD VALIDATION OF PHONE NUMBER 
            user_branch_id = get_branch_id(request)           
            obj = form.save(commit=False)
            obj.desire_date = desire_date
            obj.created_by = creator
            obj.branch_id = user_branch_id
            obj.amount_desired = request.POST.get('desired_amount',False)
            obj.save()
            msg_status = True
            msg = 'CUSTOMER SUCCESSFULLY SAVED'
            msg_status = True 
            form = Potential_Customers_Form()
        else:
            msg = form.errors
            msg_status = False   

    active = 'potential_customer'
    context = {
        'form': form,
        'msg_status': msg_status,
        'activity_data': activity_data,
        'msg': msg, 'txn_date' : get_Open_Txn_date(request),
        'msg-status': msg_status, 'active' : active,
        "currentGroup": get_user_group(request)
    }

    return render(request, 'rm/potential_customer.html', context)

def repeatPotentialCustomer(request):
    activity_data = None
    active = None
    msg = None
    form = None 
    msg_status = None
    count = None
    txn_date = get_Open_Txn_date(request)
    creator = request.user.id
    form = Repeat_Potential_Customer()
    customers = Potential_Customers.objects.filter(branch_id=get_branch_id(request) , turn_over='active_cilent', created_by=request.user.id)
    activity_data = Potential_Customers.objects.filter(created_by=creator)    
    if request.method == 'POST' and request.POST:
        customer_id = request.POST.get('customer_id', False)
        desired_amount = request.POST.get('desired_amount', False)
        get_customer = Potential_Customers.objects.get(id=customer_id)
        get_customer.amount_desired = desired_amount
        if get_customer.loan_count == 0:
            count = 2
        else:
            count = get_customer.loan_count + 1
        get_customer.loan_count = count
        get_customer.turn_over = 'potential_cilent'
        get_customer.updated_by = request.user.id
        get_customer.desire_date = txn_date
        get_customer.save()
        msg='NEW POTENTIAL SUCCESSFULLY UPDATED'
        msg_status=True
       
    active = 'potential_customer'
    context = {
        'form': form,
        'msg_status': msg_status,
        'activity_data': activity_data,
        'msg': msg, 
        'customerddl': customers,
        'txn_date' : txn_date,
        'msg-status': msg_status, 'active' : active,
        "currentGroup": get_user_group(request)
    }

    return render(request, 'rm/repeat_potential_customer.html', context)

def pendingCollections(request):
    activity_data = RM_Collection_Sheets.objects.select_related('customer').filter(collection_date = get_Open_Txn_date(request), created_by=request.user.id) 
    id = []
    for ad in activity_data:
        id.append(ad.customer.id)        
    potential_customer = Potential_Customers.objects.filter(created_by=request.user.id).exclude(id__in=id)
    msg = None
    msg_status = None
    success = None
    receipt_no = None
    active = None
    form = None
    active = 'collections_sheet'
    context = {
        'form': form,
        'msg_status': msg_status,
        'activity_data': activity_data,
        'potential_customer':potential_customer,
        'receipt_no' : receipt_no,
        'msg': msg, 
        'txn_date' : get_Open_Txn_date(request),
        'active': active,
        "currentGroup": get_user_group(request)
    }

    return render(request, 'rm/pending_collections.html', context)
    
# END RM Views
# 
# 
# START Manager Views

 
def get_branch_rms(request):
    try:
        return Profile.objects.select_related('user').filter(branch_id=get_branch_id(request), user__groups__in=[5,4])
    except:
        return None 
    



def rm_collections(request):    
    activity_data = None
    msg = None
    rms = None
    total_collections = None
    total_collections_amount = None    
    msg_status = None
    rms = get_branch_rms(request) 
    txn_date = get_Open_Txn_date(request)
    # select rm
    form = RM_Search_Collections_Form()
    if request.method == 'POST':
        table = request.POST.get('table_form', False) 
        if table:
            id_list = request.POST.getlist('id[]')
            # msg = id_list
            # update to default first
            c_sheet = RM_Collection_Sheets.objects.filter(id__in=id_list).update(authorization_status="PENDING", authorization_note="Not Authorized By Branch Manager" , updated_by=request.user.id)
            c_sheet = RM_Collection_Sheets.objects.filter(id__in=id_list).update(authorization_status="APPROVED", authorization_note="Collection Accepted" , updated_by=request.user.id)
            # activity_data = RM_Collection_Sheets.objects.filter(created_by=rm_id, collection_date=collection_date) 
            msg = 'SUCCESSFULLY APPROVED'  
            msg_status = True
        else:
            collection_date = get_date(request)# get_Open_Txn_date(request)
            #print(collection_date)
            rm_id = request.POST.get('rm', False)
            activity_data = RM_Collection_Sheets.objects.filter(created_by=rm_id, collection_date=collection_date)      
            print(activity_data)
            if not activity_data :
                msg = 'No Collections Captured by selected RM Yet'
                msg_status = False
            else:     
                total_collections = activity_data.count() 
                total_collections_amount = activity_data.aggregate(Sum('amount_collected'))          
                rms = get_branch_rms(request)
                msg = 'Rm Collection\'s ' + 'Total Collections = ' + str(total_collections)+' AND ' + 'Total Amount Collected = ' + str(total_collections_amount) 
                msg_status = True
    else:
        msg = '' 
        total_collections = ''
        total_collections_amount = ''  
       
    active = 'collections'
    context = {
        'form': form,
        'txn_date' : get_Open_Txn_date(request),
        'activity_data': activity_data,
        'msg': msg, 'msg_status': msg_status, 
        'total_collections': total_collections,
        'total_collections_amount': total_collections_amount,
        'rmddl': rms, 'active': active,
        "currentGroup": get_user_group(request)}
    return render(request, 'manager/rm_collections.html', context)

def add_disbursement(request):
    form = Disbursement_Form()
    activity_data = None
    msg = None
    msg_status = None
    customers = None
    creator = None

    # Get Potential But Find a way of changing status after save so they
    # dont app
    customers = Potential_Customers.objects.filter(branch_id=get_branch_id(request) , turn_over='potential_cilent')
    activity_data = Disbursements.objects.select_related('customer_id').filter(branch_id=get_branch_id(request)).order_by('-created_on')
    if request.method == 'POST': 
        form = Disbursement_Form(request.POST)
        if form.is_valid(): 
            creator = request.user.id
            user_branch_id = get_branch_id(request)
            customer_id = request.POST.get('customer_id', False)            
            # rm_id = request.POST.get('rm', False)
            # activity_data = RM_Collection_Sheet.objects.filter(created_by=rm_id, collection_date=collection_date)  
            # total_collections = activity_data.count() 
            # total_collections_amount = activity_data.aggregate(Sum('amount_collected'))      
            obj = form.save(commit=False)
            obj.created_by = creator
            obj.branch_id = user_branch_id
            obj.save()
            # update potential cilent to Active cilent
            Potential_Customers.objects.filter(id=customer_id).update(turn_over='active_cilent')
            msg = 'CUSTOMER DISBUREMENT SUCCESSFULLY SAVED'
            msg_status = True

        else: 
            msg = form.errors
            msg_status = False
    context = {
        'form': form, 'activity_data': activity_data,
        'msg': msg,   'msg_status': msg_status,
        'customerddl': customers,  "currentGroup": get_user_group(request) }
    return render(request, 'manager/add_disbursement.html', context)

def view_disbursement(request):
    form = Disbursement_Search_Form()
    activity_data = None
    msg = None
    msg_status = None
    customers = None
    creator = None
    current_user_groups = request.user.groups.values_list("name", flat=True)
           
    if request.method == 'POST':
        form = Disbursement_Search_Form(request.POST)
        if form.is_valid():
            activity_data = Disbursements.objects.select_related('customer_id').filter(branch_id=get_branch_id(request), disbursed_date=form.cleaned_data['disbursed_date']).order_by('-created_on')       
        else:
            msg_status = False
            msg = form.errors
            
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg, 'msg_status': msg_status,
        'active': 'view_disbuse' ,"currentGroup": get_user_group(request)
        
        }
    return render(request, 'manager/view_disbursement.html', context)


def post_authorization(request):

    rms = Profile.objects.select_related('user').filter(branch_id=get_branch_id(request), user__groups__in=[5])
    msg = None 
    form = None
    id_list = None
    if request.method == 'POST' and request.POST:       
        id_list = request.POST.getlist('id[]')
        msg = id_list
        collection_date = get_Open_Txn_date(request)
        # update to default first
        c_sheet = RM_Collection_Sheets.objects.update(authorization_status="PENDING", authorization_note="Not Authorized By Branch Manager" , updated_by=request.user.id)
        c_sheet = RM_Collection_Sheets.objects.filter(id__in=id_list).update(authorization_status="APPROVED", authorization_note="Collection Accepted" , updated_by=request.user.id)
        msg = 'SUCCESSFULLY APPROVED'     
       
    else:
        msg = "no post"
       
    context = {
        'form': form, 
        'rmddl': rms,
        'msg': msg,
        'idlist': id_list,  "currentGroup": get_user_group(request)}
    return  render(request, 'manager/rm_collections.html', context)

def add_daily_report(request):
    form = None
    activity_data = None
    msg = None
    msg_status = None
    form = Daily_Report_Form()
    collections = getTotalCollections(request)
    # disbursements = getTotalDisbursement(request)
    # clients_Disbursed = getTotalClientsDisbursed(request)
    if request.POST:       
        form = Daily_Report_Form(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.branch_id = get_branch_id(request)
            obj.created_by = request.user.id
            obj.total_collections = collections
            obj.activity_date = get_Open_Txn_date(request)
            # obj.total_disbursed = disbursements
            # obj.total_clients_disbursed = clients_Disbursed
            obj.save()
            msg = "Daily Report Successfully Saved"
            msg_status = True
        else:
            msg = form.errors
            msg_status = False   
    
    active = 'daily_report'
    context = {
        'form': form, 
        'activity_data': activity_data,
        'txn_date' : get_Open_Txn_date(request),
        'msg': msg, 
        'msg_status': msg_status,
        "active":active,
        "currentGroup": get_user_group(request),
        "collections" : collections
        }
    return render(request, 'manager/add_daily_report.html', context)

def manage_rm(request):
    active = 'manage_rm'
    msg = None
    msg_status = None
    form = None
    activity_data = None
    branch_id=get_branch_id(request)
    # activity_data =  Profile.objects.filter() #, user__groups__in=5
    activity_data = Profile.objects.select_related('user').filter(branch_id=branch_id, user__groups__in=[5])
    # Profile.objects.select_related('user').filter(branch_id=get_branch_id(request), user__groups__in=5) .select_related('user')
    
    form = SignUpForm(request.POST)
    
    if request.method == 'POST':        
        # call the group model and insert the created user but first get the 
        # user_id of the last inserted user
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            my_group = Group.objects.get(name='RM') 
            my_group.user_set.add(user)
            mrg_profile = Profile.objects.get(user_id=request.user.id)
            mrg_branch = Branch.objects.get(id=mrg_profile.branch_id_id)
            my_profile = Profile.objects.create(
                user=user,
                location=mrg_profile.location,
                branch_id=mrg_branch,
                created_by= int(request.user.id),
                created_on = date.today()
                )           
            msg     = str(user) + ' created '
            success = True
            
            #return redirect("/login/")

        else:
            msg = 'Form is not valid' 
    
            
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg, 
        'msg_status': msg_status,
        "active":active,
        'txn_date' : get_Open_Txn_date(request),
        "currentGroup": get_user_group(request)
        }
    return render(request, 'manager/manage_rm.html', context)

def rm_reassignment(request):
    form = None
    activity_data = None
    msg = None
    msg_status = None
    rm_ddl = None
    active = None  
    cust  = None
    active = 'manage_rm'
    mylist = []
    rm_ddl = get_branch_rms(request)
    #activity_data = Potential_Customers.objects.filter(branch_id=get_branch_id(request));
    activity_data = Potential_Customers.objects.values('created_by', 'reassigned_to').annotate(
        dcount=Count('created_by'), rcount=Count('reassigned_to')).order_by()
    
     
    if request.method == 'POST' and request.POST:        
        rm_from = request.POST.get('rm_from',False)
        rm_to = request.POST.get('rm_to',False)
        from_rms_customer = Potential_Customers.objects.filter(turn_over='active_cilent', created_by=rm_from)
        for cust in from_rms_customer:
            mylist.append(cust.id)
        
        assign_customers = Potential_Customers.objects.filter(id__in=mylist).update(reassigned_to=rm_to, reassigned_by=request.user.id , updated_by=request.user.id) 
        #to_rms_customer = Potential_Customers.objects.filter(turn_over='active_cilent', created_by=rm_to)
        
        msg = assign_customers + " Customers have been reassigned"#str(rm_from) + " " + str(rm_to)
        msg_status = True
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg, 
        'msg_status': msg_status,
        "active":active,
        "rmddl":rm_ddl,       
        'txn_date' : get_Open_Txn_date(request),
        "currentGroup": get_user_group(request)
        }
    return render(request, 'manager/rm_reassignment.html', context)
# END Manager Views table

