# from django import forms
# import datetime
# from datetime import date, timedelta
# from app.models import RM_Collection_sheet, Potential_Customers


# class Collection_Sheet_Form(forms.ModelForm):
#     collection_date = forms.DateField(
#         required=True,
#         initial=datetime.date.today,
#         widget=forms.SelectDateWidget(
#             attrs={"class":"form-control form-control-sm"}
#             )
#         )
#     customer_name = forms.CharField(
#             required=True,
#             widget=forms.TextInput(attrs={
#                     "placeholder": "Enter Customer Name",                
#                     "class": "form-control form-control-sm"
                
#                 })
#         )
#     amount_collected = forms.DecimalField(
#         required=True,
#         label='Amounted For By Customer',         
#         widget=forms.TextInput(attrs={
#                 "placeholder": "Enter Amounted For By Customer",                
#                 "class": "form-control form-control-sm",
#                 "oninput": "digitsep(this)",
#                 "id": "amount_collected",
#                "min" : "0"
              
#             })
#         )
#     receipt_number = forms.IntegerField(
#         required=True,
#         label='Receipt Number',    
#         widget=forms.NumberInput(attrs={
#                 "placeholder": "Enter Receipt Number",                
#                 "class": "form-control form-control-sm",              
#                 "min" : "0",
#                 "id":"receipt_no"             
#             }))
#     created_by = forms.CharField( required=False,
#         widget=forms.HiddenInput(attrs={
#                 "placeholder": "Created by",                
#                 "class": "form-control"               
#             })
#     )
#     class Meta:
#         model = RM_Collection_Sheet
#         fields = (
#             'customer_name', 
#             'amount_collected', 
#             'receipt_number',
#             'collection_date',
#             'created_by'
#             )


# class Potential_Customers_Form(forms.ModelForm):

    # first_name = forms.CharField( required=True,
    #  label='First Name', 
    #         widget=forms.TextInput(attrs={
    #                 "placeholder": "Enter First Name",                
    #                 "class": "form-control form-control-sm"
                
    #             })
    #     )
    # last_name = forms.CharField( required=True,
    #  label='Last Name', 
    #         widget=forms.TextInput(attrs={
    #                 "placeholder": "Enter Last Name",                
    #                 "class": "form-control form-control-sm"
                
    #             })
    #     )
#     contact = forms.CharField( required=True,
#      label='Customer Contact', 
#             widget=forms.TextInput(attrs={
#                     "placeholder": "Enter Customer Contact Number",                
#                     "class": "form-control form-control-sm",
#                     "max": "10"
                
#                 })
#         )
#     business_type = forms.CharField( required=True,
#      label='Business Type', 
#             widget=forms.TextInput(attrs={
#                     "placeholder": "Enter Business Type",                
#                     "class": "form-control form-control-sm"
                
#                 })
#         )
#     business_location = forms.CharField( required=True,
#      label='Business Location', 
#             widget=forms.TextInput(attrs={
#                     "placeholder": "Enter Business Location",                
#                     "class": "form-control form-control-sm"                
#                 })
#         )
#     desired_date = forms.DateField(
#          label='Date', 
#         required=True,
#         initial=datetime.date.today,
#         widget=forms.SelectDateWidget(
#             attrs={"class":"form-control form-control-sm"}
#             )
#         )
#     desired_amount = forms.DecimalField(
#         required=True,
#         label='Amounted Desired',         
#         widget=forms.TextInput(attrs={
#                 "placeholder": "Enter Amount Wanted By Customer",                
#                 "class": "form-control form-control-sm",
#                 "oninput": "digitsep(this)",
#                 "id": "desired_amount",
#                 "min" : "0"
              
#             })
#         )
#     created_by = forms.CharField( required=False,
#         widget=forms.HiddenInput(attrs={
#                 "placeholder": "Created by",                
#                 "class": "form-control"               
#             })
#     )
#     class Meta:
#         model = Potential_Customers
#         fields = (
#             'first_name',
#             'last_name',
#             'desired_amount',
#             'contact',
#             'business_type',
#             'business_location',
#             'desired_date',
#             'created_by'
#         )
