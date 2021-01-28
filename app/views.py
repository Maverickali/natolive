# -*- encoding: utf-8 -*-
"""
Copyright (c) 
"""

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from django.urls import reverse
from django.utils import timezone
from django.views import generic 
from django.db.models import Sum
from app.forms import RMWeeklyCustomersForm, RMWeeklyCustomersPortfolioForm, RmDailyActivityForm, SearchForm, SetTargetsForm, TargetsPortfoiloForm, TreasuryForm
from .functions import branch_disable
from app.models import Branch, Injections, Profile, RM_Daily_Activity
import datetime
from datetime import date, timedelta
import re
from django.contrib.auth.models import User



@login_required(login_url="/login/")
def index(request):    
    cash_forward = Injections.objects.aggregate(Sum('cash_forward'))
    
    context = { 'cash_forward': cash_forward['cash_forward__sum']}
    context['segment'] = 'index'
    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def treasury_create(request):

    msg     = None
    success = False
    current_user_groups = request.user.groups.values_list("name", flat=True)
    if request.method == 'POST' and request.POST:
        form = TreasuryForm(request.POST)
        if form.is_valid():            
            obj = form.save(commit=False)
            obj.created_by = request.user.id
            obj.cash_reserve_need = float(request.POST['cash_forward']) - (float(request.POST['new_customer_amount']) + float(request.POST['repeat_customer_amount']))
            obj.save()
            success = True 
            msg = 'Treasury Report Successfully Saved'
        else:
            msg='FORM IS INVALID'
    else:
        form = TreasuryForm()
    user_name = request.user.username
    form = branch_disable(user_name,'treasury')
    context = {
        'form': form, 
        "msg" : msg, 
        "success" : success, 
        "currentGroup": current_user_groups}

    return render(request, 'treasury/create.html', context)
    
def treasury_report(request):

    treasury_list = None
    msg = ''
    updated = None
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

            if inj_status == 'on':
                inj_status = True
            else:
                inj_status = False

            if all_branchs == 'on':
                treasury_list = Injections.objects.filter(injection_status=inj_status, date__range=(from_date, to_date)).order_by('-date')               
            else:
                all_branchs = False           
                treasury_list = Injections.objects.filter(injection_status=inj_status, date__range=(from_date, to_date), branch_name=branch_id).order_by('-date')
            search_form = SearchForm().full_clean()
        else:
            updated = False
            msg = "VALIDATION FAILED"
    else:
        search_form = SearchForm()
        treasury_list = Injections.objects.filter(injection_status=True,date=datetime.datetime.today()).order_by('-date')
    msg = Injections.objects.aggregate(Sum('cash_forward'))
    branch_name = Branch.objects.all()
    user_name = request.user.username    
    search_form = branch_disable(user_name,'search')
    context = { 
            'treasuryList': treasury_list, 
            'searchform': search_form,
            'Branch': branch_name, 'updated': updated, 'msg': msg}

    return render(request, 'treasury/view.html', context)

def approved_injection(request, id):

    treasury_list = None
    treasury_list = Injections.objects.filter(injection_status=True,date=datetime.datetime.today()).order_by('-date') 
    updating = None
    msg = None
    if request.user.has_perm('app.can_approve_reject_injection'):     
        # Injections.objects.all()   
        updated = Injections.objects.select_related().get(record_id=id)
        # treasury_list = updated
        updated.injection_authorization = 'APPROVED'
        updated.injection_status = False
        updated.updated_by = request.user.id
        updated.save()
        updated = True  
        msg = 'Injection Approved Successfully'
    else:
        return render(request, 'includes/noauthorization.html')
    search_form = SearchForm()
    context = { 
        'treasuryList' : treasury_list, 
        'searchform': search_form,
        'updated': updated, 
        'msg': msg}
    return render(request, 'treasury/view.html', context)

def rejected_injection(request, id):
    treasury_list = None
    try:
        msg = None
        success = None
        if request.user.has_perm('app.can_approve_reject_injection'):     
            treasury_list = Injections.objects.filter(injection_status=True,date=datetime.datetime.today()).order_by('-date')
            updated = Injections.objects.select_related().get(record_id=id)
            updated.injection_authorization = 'REJECTED'
            updated.injection_status = False
            updated.updated_by = request.user.id
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
        'updated': updated, 
        'msg': msg}
    return render(request, 'treasury/view.html', context)


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
    context = {}
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
                obj.before_authorization = "PENDING-APPROVAL"                
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
                obj.before_authorization = "PENDING-APPROVAL"                
                obj.save()
                success = True 
                msg = 'SUCCESSFULLY SAVED'
            else:
                msg= form.errors

    else:
        msg='.'        
    
    form = RMWeeklyCustomersPortfolioForm()
    frm = RMWeeklyCustomersForm()       

    context = {
        'form': form, 
        'frm': frm, 
        "msg": msg, 
        "success": success,
        "currentGroup": current_user_groups}

    return render(request, 'rm/create_weekly_assessments.html', context)

def rm_weekly_assessments_view(request):
    pass

def set_targets(request):
    msg = None
    user = User.objects.all()    
    # Geting the branch id from the profile list
    id = request.user.profile.branch_id_id
    profile = Profile.objects.filter(branch_id_id=id)
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
        'msg': msg, 'profile': profile, 'user' : user}
    return render(request, 'manager/set_targets.html', context)

def set_targets_view(request):
    pass
