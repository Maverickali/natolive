from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Sum
from app.forms import SearchForm, TreasuryForm
import re
import datetime
from datetime import date, timedelta
from app.models import Branch, Disbursements, Potential_Customers, Profile, RM_Collection_Sheets
from eod.models import Eod
from id_manager.models import Ids
import random
import string
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail
from clusters.models import Assignments, Cluster_branches, Clusters



def mail(request, subject, message, recipient_list):
    # subject = 'welcome to GFG world'
    # message = f'Hi Collins, thank you for registering in geeksforgeeks.'
    email_from = settings.EMAIL_HOST_USER
    # recipient_list = ["collinsmaverick11@gmail.com"]
    return send_mail(subject, message, email_from, recipient_list )
    

def group_required(request, *group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(user):
        if request.user.is_authenticated():
            if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url='/login/')


def branch_disable(user_name, form):
    res = re.split('\d*\D+',user_name)
    if form == 'search':
        form = SearchForm(initial={'branch_name': str(res[1])}, auto_id=False)        
    else:
        form = TreasuryForm(initial={'branch_name': str(res[1])}, auto_id=False)
        
    if len(str(res[1])) != 0:
        form.fields['branch_name'].disabled = True
        # _form.fields['branch_name'].disabled = True
    return form


def clean_form(form):
    return form.full_clean()

def get_date(request):
    year = int(request.POST['collection_date_year'])
    month = int(request.POST['collection_date_month'])
    day = int(request.POST['collection_date_day'])
    return datetime.date(year,month,day)

def get_desire_date(request):
    year = int(request.POST['desired_date_year'])
    month = int(request.POST['desired_date_month'])
    day = int(request.POST['desired_date_day'])
    return datetime.date(year,month,day)
    
def get_branch_id(request):
    try:
        profile = Profile.objects.get(user_id=request.user.id)
        return profile.branch_id_id 
    except ObjectDoesNotExist:
        return 0
        

def get_user_group(request):
    return request.user.groups.values_list("name", flat=True)

def getTotalClientsDisbursed(request):
    clients = Disbursements.objects.filter(branch_id=get_branch_id(request)).count()
    return clients

def getTotalCollections(request):
    collections = RM_Collection_Sheets.objects.filter(authorization_status='APPROVED'
                                                      ,branch_id=get_branch_id(request)
                                                      ,collection_date=get_Open_Txn_date(request)   ).aggregate(Sum('amount_collected'))
    return collections["amount_collected__sum"]

def getTotalDisbursement(request):
    disbursement = Disbursements.objects.filter(branch_id=get_branch_id(request)).aggregate(Sum('amount_disbursed'))
    return disbursement["amount_disbursed__sum"]

def create_unique_id():
    return ''.join(random.choices(string.digits, k=6))

def get_branch_account_number(request):
    #Ids = None   
    branch_id = get_branch_id(request)
    account_number = str(branch_id) + create_unique_id()
    unique = False
    while not unique:
        try:          
            if not Ids.objects.filter(account_number=account_number):
                unique = True
            else:
                account_number = create_unique_id() 
        except Ids.DoesNotExist:
            pass
         
    return account_number 


def get_Open_Txn_date(request): 
    branch_id = get_branch_id(request)
    try:
        branch = Branch.objects.get(id=branch_id)
    except ObjectDoesNotExist:
        return     
    try:
        txn = Eod.objects.get(branch_id=branch, is_closed=0)
        txn_date = txn.transaction_date        
    except ObjectDoesNotExist :        
        eod_ = Eod.objects.get_or_create(
                    branch_id=branch,
                    transaction_date=datetime.date.today() )
        txn_date = Eod.objects.get(branch_id=branch_id, is_closed=0).transaction_date
    return txn_date

def get_branch_supervisors():
    try:
        return User.objects.select_related('user').filter( user__groups__in=[2,4])
    except:
        return None 
    
def getSupaClustorBranches(request):
    cluster = Assignments.objects.select_related('user_id', 'cluster_branch_id', 'cluster_id').filter(user_id=request.user.id).values('cluster_branch_id_id__cluster_id' )
    for b in cluster:
        cluster_id = b
    cluster_instance = Clusters.objects.get(id=cluster_id['cluster_branch_id_id__cluster_id'])
    # Supervisor's cluster class
    branches = Cluster_branches.objects.filter(cluster_id=cluster_instance)
    return branches