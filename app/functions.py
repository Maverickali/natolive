from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate
from django.db.models import Sum
from app.forms import SearchForm, TreasuryForm
import re
import datetime
from app.models import Disbursements, Potential_Customers, Profile, RM_Collection_Sheets





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

def get_date(request):
    pass

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
    profile = Profile.objects.get(user_id=request.user.id)
    return profile.branch_id_id 

def get_user_group(request):
    return request.user.groups.values_list("name", flat=True)

def getTotalClientsDisbursed(request):
    clients = Disbursements.objects.filter(branch_id=get_branch_id(request)).count()
    return clients

def getTotalCollections(request):
    collections = RM_Collection_Sheets.objects.filter(authorization_status='APPROVED').aggregate(Sum('amount_collected'))
    return collections["amount_collected__sum"]

def getTotalDisbursement(request):
    disbursement = Disbursements.objects.filter(branch_id=get_branch_id(request)).aggregate(Sum('amount_disbursed'))
    return disbursement["amount_disbursed__sum"]
