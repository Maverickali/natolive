# from app.rm_forms import Potential_Customers_Form, Collection_Sheet_Form
# from .functions import branch_disable, get_branch_id
# from app.models import Potential_Customers, Branch, Profile, RM_Collection_Sheet
# from app.functions import clean_form, get_date
# from django.db import DatabaseError
# from logging import exception


# def rm_collection_sheet(request):
    
#     activity_data = RM_Collection_Sheet.objects.all()
#     msg = None
#     msg_status = None
#     success = None
#     # Post 
    
#     if request.method == 'POST' and request.POST:
#         form = Collection_Sheet_Form(request.POST)        
#         if form.is_valid():
#             collection_date = get_date(request)
#             receipt_no = request.POST['receipt_number']
#             creator = request.user.id
#             checker = None
            
#             try:
#                 # Go to db
#                 checker = RM_Collection_Sheet.objects.get(receipt_number=receipt_no)
#                 if not checker :
                    
#                     obj = form.save(commit=False)
#                     obj.created_by = creator
#                     # obj.collection_date = collection_date
#                     obj.before_authorization = "PENDING"
#                     obj.save()
#                     msg_status = True
#                     msg = 'SUCCESSFULLY SAVED'
#                     form = Collection_Sheet_Form().full_clean()
#                     form = Collection_Sheet_Form()
                    
#                 else:
#                     msg = "You have Already Used this Receipt number CAN'T SAVE THIS COLLECTION"
#                     msg_status = False

#             except DatabaseError as e:
#                 msg = e  
#                 msg_status = False             
#         else:
#             msg = form.errors
#             msg_status = False
#     else:
#         form = Collection_Sheet_Form()

#     context = {
#         'form': form,
#         'msg_status': msg_status,
#         'activity_data': activity_data,
#         'msg': msg
#     }

#     return render(request, 'rm/c_collection_sheet.html', context)

# def potential_customer(request):
#     activity_data = None
#     msg = None
#     form = None 
#     msg_status = None
#     creator = request.user.id
#     form = Potential_Customers_Form()
#     activity_data = Potential_Customers.objects.filter(created_by=creator)    
#     if request.method == 'POST' and request.POST:
#         form = Potential_Customers_Form(request.POST)
#         if form.is_valid():
#             # ADD VALIDATION OF PHONE NUMBER 
#             user_branch_id = get_branch_id(request)
#             msg = Profile.objects.get(user_id=request.user.id).branch_id_id
#             obj = form.save(commit=False)
#             obj.created_by = creator
#             obj.branch_id = user_branch_id
#             obj.save()
#             msg_status = True
#             msg = 'CUSTOMER SUCCESSFULLY SAVED'
#             form = Potential_Customers_Form()
#         else:
#             msg = form.errors
#             msg_status = False   


#     context = {
#         'form': form,
#         'msg_status': msg_status,
#         'activity_data': activity_data,
#         'msg': msg,
#         'msg-status': msg_status
#     }

#     return render(request, 'rm/potential_customer.html', context)
