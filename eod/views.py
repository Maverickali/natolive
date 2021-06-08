from django.shortcuts import render
from app.models import Branch, RM_Collection_Sheets
from .models import Eod
from app.functions import get_branch_id, get_user_group, get_Open_Txn_date, getTotalCollections
import datetime
from django.db.models import ObjectDoesNotExist

# Create your views here.
def eod(request):
    msg = None
    msg_status = None
    success = False
    active = 'eod'
    try:
        branch = Branch.objects.get(id=get_branch_id(request))
    except ObjectDoesNotExist:
        context = {
        'activity_data':"",
        'txn_date': "",
        "msg": "ERROR OCCURED PLEASE CONTACT THE ADMINISTRATOR", 
        'msg_status': False ,
        "success": success,
        "currentGroup": get_user_group(request), 
        'active':active}
        return render(request, 'manager/eod.html', context)
    activity_data = Eod.objects.filter(branch_id=get_branch_id(request))
    txn_date = get_Open_Txn_date(request)
    if request.method == 'POST' and request.POST:
        id_ = request.POST.get('id', False)
        pending_collections = RM_Collection_Sheets.objects.filter(
            authorization_status='PENDING'
            ,branch_id=get_branch_id(request)
            ,collection_date=txn_date)
        
        if not pending_collections:
            updated = Eod.objects.update(is_closed=True,closed_on=txn_date,days_collections=getTotalCollections(request),update_on=datetime.datetime.now(),closed_by=request.user.id)
            # create new EOD
            # If Manager hasnt closed for days system should automatically Close use Python Celery to make queue task for version 2 nato 
            new_day = datetime.datetime.now() + datetime.timedelta(days=1)
            branch_id = get_branch_id(request)
            branch = Branch.objects.get(id=branch_id)
            eod_ = Eod.objects.get_or_create(branch_id=branch,transaction_date=new_day)
        else: 
            msg='You cant Closed the Day with collections transactions PENDING Approval'
            msg_status = False 
        
    context = {
        'activity_data':activity_data,
        'txn_date': txn_date,
        "msg": msg, 
        'msg_status': msg_status ,
        "success": success,
        "currentGroup": get_user_group(request), 
        'active':active}

    return render(request, 'manager/eod.html', context)
