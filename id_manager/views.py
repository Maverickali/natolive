from django.shortcuts import render
from app.manager_forms import Add_ID_Form
from app.models import Disbursements, Potential_Customers, Profile
from app.functions import get_branch_id, get_user_group
from id_manager.models import Ids
from _datetime import date

# Create your views here.

def add_id(request):
    form = Add_ID_Form()
    activity_data = None
    msg = None
    msg_status = None
    customers = None
    creator = None
    active = 'add_id'
    # Get Potential But Find a way of changing status after save so they
    # dont app
    # id status 
    # submitted - when submitting id to crown house
    # Received_By_Id_Manager - when crown house gets id from branch
    # Requested - when branch-manager wants to get an id from crown house
    # Withdrawn - when id leaves crown house to branch-manager
    # Received_By_Branch_Manager - when branch-manager recevices the id from the crown house
    # Return_To_Customer - when branch-manager gives id back to the customer

    customers = Potential_Customers.objects.filter(branch_id=get_branch_id(request) , turn_over='potential_cilent')
    activity_data = Ids.objects.select_related('customer_id').filter(branch_id=get_branch_id(request)).order_by('id')
    if request.method == 'POST': 
        form = Add_ID_Form(request.POST)
        if form.is_valid():
            # Flagging 
            id_checking = id_checker(request)
            if not id_checking:
                creator = request.user.id
                user_branch_id = get_branch_id(request)
                customer_id = request.POST.get('customer_id', False)            
                obj = form.save(commit=False)
                obj.created_by = creator
                obj.id_loan_count = 1
                obj.branch_id_id = user_branch_id
                obj.resubmission_date = date.today()        
                obj.save()
                # update potential cilent to Active cilent
                Potential_Customers.objects.filter(id=customer_id).update(turn_over='active_cilent')
                msg = 'CUSTOMER ID SUCCESSFULLY SAVED'
                msg_status = True
            else:
                msg = "The National ID  " + str(id_checking[0].id_number) + " is still already held by Nato " + str(id_checking[0].branch_id_id) + ". Please contact the Branch Manager holding this ID to clear it"
                msg_status = False
                

        else: 
            msg = form.errors
            msg_status = False
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        'customerddl': customers,  
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'manager/add_ID_details.html', context)


def id_checker(request):
    
    id_ = Ids.objects.select_related('customer_id').filter(
        id_number=request.POST.get('id_number', False) , 
        id_status__in=['submitted', 'Received_By_Id_Manager', 'Requested', 'Withdrawn', 'Received_By_Branch_Manager'],
        id_override_status='no').order_by('-created_on')
    return id_
    
def view_ids(request):
    form = None
    activity_data = None
    msg = None
    msg_status = None
    customers = None
    creator = None
    active = 'add_id'
    activity_data = Ids.objects.select_related('customer_id').filter(branch_id=get_branch_id(request)).order_by('-created_on')
   
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        'customerddl': customers,  
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'manager/view_IDs.html', context)

def id_request(request, id):
    form = None
    activity_data = None
    msg = None
    msg_status = None
    customers = None
    creator = None
    active = 'add_id'
    activity_data = Ids.objects.select_related('customer_id').filter(branch_id=get_branch_id(request)).order_by('-created_on')
    # add checker for who can do this
    Ids.objects.filter(id=id).update(id_status='Requested')
    msg='ID status has been successfully updated'
    msg_status=True   
        
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        'customerddl': customers,  
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'manager/view_IDs.html', context)

def id_receviced(request, id):
    form = None
    activity_data = None
    msg = None
    msg_status = None
    customers = None
    creator = None
    active = 'add_id'
    activity_data = Ids.objects.select_related('customer_id').filter(branch_id=get_branch_id(request)).order_by('-created_on')
    # add checker for who can do this
    Ids.objects.filter(id=id).update(id_status='Received_By_Branch_Manager')
    msg='ID status has been successfully updated'
    msg_status=True   
        
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        'customerddl': customers,  
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'manager/view_IDs.html', context)

def over_ride_reason(request):
    form = None
    activity_data = None
    msg = None
    msg_status = None
    customers = None
    creator = None
    active = 'add_id'
    activity_data = Ids.objects.select_related('customer_id').filter(branch_id=get_branch_id(request)).order_by('-created_on')
    if request.method == 'POST': 
        id_ = request.POST.get('id', False)
        reason = request.POST.get('reason', False)
        over_ride_status = 'yes'
        Ids.objects.filter(id=id_).update(id_status='Return_To_Customer', id_override_status=over_ride_status, id_override_reason=reason)
        msg='Over Ride Reason Successfully update'
        msg_status=True   
        
    context = {
        'form': form, 
        'activity_data': activity_data,
        'msg': msg,   
        'msg_status': msg_status,
        'active': active,
        'customerddl': customers,  
        "currentGroup": get_user_group(request) 
        }
    
    return render(request, 'manager/view_IDs.html', context)