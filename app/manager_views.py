# from django.contrib.auth.decorators import login_required, permission_required
# from django.shortcuts import render, get_object_or_404, redirect
# from django.template import loader
# from django.http import HttpResponse
# from django import template
# from django.urls import reverse
# from django.utils import timezone
# from django.views import generic 
# from django.db.models import Sum
# from app.forms import RMWeeklyCustomersForm, RMWeeklyCustomersPortfolioForm, RmDailyActivityForm, SearchForm, SetTargetsForm, TargetsPortfoiloForm, TreasuryForm
# from app.manager_forms import Daily_Report_Form, Disbursement_Form, Disbursement_Search_Form, RM_Collection_Sheets, RM_Search_Collections_Form
# from .functions import branch_disable
# from app.models import Disbursements, Potential_Customers, Branch, Injections, Profile, RM_Collection_Sheet
# import datetime
# from datetime import date, timedelta
# import re
# from django.contrib.auth.models import User
# from app.functions import clean_form, get_branch_id, get_date


# def get_branch_rms(request):
#     return Profile.objects.select_related('user').filter(branch_id=get_branch_id(request), user__groups__in=[5,4])


# def rm_collections(request):    
#     activity_data = None
#     msg = None
#     rms = None
#     total_collections = None
#     total_collections_amount = None    
#     msg_status = None
#     rms = get_branch_rms(request) 
#     # select rm
#     form = RM_Search_Collections_Form()
#     if request.method == 'POST':
#         collection_date = get_date(request)
#         rm_id = request.POST.get('rm', False)
#         activity_data = RM_Collection_Sheet.objects.filter(created_by=rm_id, collection_date=collection_date)      
#         if not activity_data :
#             msg = 'No Collections Captured by selected RM Yet'
#             msg_status = False
#         else:     
#             total_collections = activity_data.count() 
#             total_collections_amount = activity_data.aggregate(Sum('amount_collected'))          
#             rms = get_branch_rms(request)
#             msg = 'Rm Collection\'s ' + 'Total Collections = ' + str(total_collections)+' AND ' + 'Total Amount Collected = ' + str(total_collections_amount)
#             msg_status = True
#     else:
#         msg = '' 
#         total_collections = ''
#         total_collections_amount = ''  
       
  
#     context = {
#         'form': form,
#         'activity_data': activity_data,
#         'msg': msg, 'msg_status': msg_status, 
#         'total_collections': total_collections,
#         'total_collections_amount': total_collections_amount,
#         'rmddl': rms}
#     return render(request, 'manager/rm_collections.html', context)

# def add_disbursement(request):
#     form = Disbursement_Form()
#     activity_data = None
#     msg = None
#     msg_status = None
#     customers = None
#     creator = None

#     # Get Potential But Find a way of changing status after save so they
#     # dont app
#     customers = Potential_Customers.objects.filter(branch_id=get_branch_id(request) , turn_over='potential_cilent')
#     activity_data = Disbursements.objects.select_related('customer_id').filter(branch_id=get_branch_id(request)).order_by('-created_on')
#     if request.method == 'POST': 
#         form = Disbursement_Form(request.POST)
#         if form.is_valid(): 
#             creator = request.user.id
#             user_branch_id = get_branch_id(request)
#             customer_id = request.POST.get('customer_id', False)            
#             # rm_id = request.POST.get('rm', False)
#             # activity_data = RM_Collection_Sheet.objects.filter(created_by=rm_id, collection_date=collection_date)  
#             # total_collections = activity_data.count() 
#             # total_collections_amount = activity_data.aggregate(Sum('amount_collected'))      
#             obj = form.save(commit=False)
#             obj.created_by = creator
#             obj.branch_id = user_branch_id
#             obj.save()
#             # update potential cilent to Active cilent
#             Potential_Customers.objects.filter(id=customer_id).update(turn_over='active_cilent')
#             msg = 'CUSTOMER DISBUREMENT SUCCESSFULLY SAVED'
#             msg_status = True

#         else: 
#             msg = form.errors
#             msg_status = False
#     context = {
#         'form': form, 'activity_data': activity_data,
#         'msg': msg,   'msg_status': msg_status,
#         'customerddl': customers }
#     return render(request, 'manager/add_disbursement.html', context)

# def view_disbursement(request):
#     form = Disbursement_Search_Form()
#     activity_data = None
#     msg = None
#     msg_status = None
#     customers = None
#     creator = None       
#     if request.method == 'POST':
#         form = Disbursement_Search_Form(request.POST)
#         if form.is_valid():
#             activity_data = Disbursements.objects.select_related('customer_id').filter(branch_id=get_branch_id(request), disbursed_date=form.cleaned_data['disbursed_date']).order_by('-created_on')       
#         else:
#             msg_status = False
#             msg = form.errors
            
#     context = {
#         'form': form, 
#         'activity_data': activity_data,
#         'msg': msg, 'msg_status': msg_status
#         }
#     return render(request, 'manager/view_disbursement.html', context)


# def post_authorization(request):

#     rms = Profile.objects.select_related('user').filter(branch_id=get_branch_id(request), user__groups__in=5)
#     msg = None 
#     form = None
#     id_list = None

#     if request.method == 'POST' and request.POST:
#         # if form.is_valid:                
#         form = RM_Collection_Sheets(request.POST) 
#         id_list = request.POST.getlist('id[]')
#         msg = id_list
#         collection_date = get_date(request)
#         # update to default first
#         c_sheet = RM_Collection_Sheet.objects.update(before_authorization="PENDING", authorization_note="Not Authorized By Branch Manager" , updated_by=request.user.id)
#         c_sheet = RM_Collection_Sheet.objects.filter(id__in=id_list).update(before_authorization="APPROVED", authorization_note="Collection Accepted" , updated_by=request.user.id)
#         msg = 'SUCCESSFULLY SAVED'
#         # else:
#         #     msg = form.errors
       
#     else:
#         msg = "no post"
       
#     context = {
#         'form': form, 
#         'rmddl': rms,
#         'msg': msg,
#         'idlist': id_list}
#     return render(request, 'manager/rm_collections.html', context)

# def add_daily_report(request):
#     form = None
#     activity_data = None
#     msg = None
#     msg_status = None
#     form = Daily_Report_Form()   
    
    
#     context = {
#         'form': form, 
#         'activity_data': activity_data,
#         'msg': msg, 'msg_status': msg_status
#         }
#     return render(request, 'manager/add_daily_report.html', context)