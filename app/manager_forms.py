
from django import forms
import datetime
from app.models import Daily_Report, Disbursements, Branch, Profile, RM_Collection_Sheets, RM_Daily_Activity, RM_Weekly_Customers, RM_Weekly_Customers_Portfolio, Targets_Collections_Disbursement, Targets_Portfoilo
from datetime import date, timedelta
from app.functions import get_branch_id
from django.forms.widgets import DateInput


class RM_Search_Collections_Form(forms.Form):
    collection_date = forms.DateField(
        required=True,
        initial=datetime.date.today,
        widget=forms.SelectDateWidget(
            attrs={"class": "form-control form-control-sm"}
            )
        )

    # class Meta:
    #     model = RM_Collection_Sheet
    #     fields = ['collection_date']
    

class Disbursement_Form(forms.ModelForm):

    amount_disbursed = forms.DecimalField(
        required=True,
        label='Amounted For By Customer',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Amount Wanted By Customer",                
                "class": "form-control form-control-sm",
                "oninput": "digitsep(this)",
                "id": "desired_amount",
                "min" : "0"
              
            })
        )  
    id_number = forms.CharField( 
        required=True,
        label='NIM Number', 
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Customer's NIM Number",                
                "class": "form-control form-control-sm"                
            })
        )
    class Meta:
        model = Disbursements
        fields = (
            'amount_disbursed',
            'disbursed_date',
            'id_number', 'customer_id'               
        )
        widgets = {
            'disbursed_date': DateInput(attrs={'type': 'date','class': 'form-control form-control-sm'}),          
           
        }
        
        
class Disbursement_Search_Form(forms.ModelForm):
    branch_id = forms.CharField(        
        label='Select Branch', 
        required=False,
        max_length=50,
        widget=forms.Select(
            attrs={"class": "form-control form-control-sm", "id": "branchSelector"}, 
            choices=[(b.id, b.branch_name) for b in Branch.objects.all()]
            ),
    )
    
    class Meta:
        model = Disbursements  
        fields = (
            'branch_id',
            'disbursed_date'
        )     
        widgets = {
            'disbursed_date': DateInput(attrs={'type': 'date','class': 'form-control form-control-sm'}),
        }
 
class Daily_Report_Form(forms.ModelForm):
    branch_id = forms.CharField(        
        label='Select Branch', 
        required=False,
        max_length=50,
        widget=forms.Select(
            attrs={"class": "form-control form-control-sm", "id": "branchSelector"}, 
            choices=[(b.id, b.branch_name) for b in Branch.objects.all()]
            ),
    )
    
    opening_bal = forms.DecimalField(
        required=True,
        label='Opening Balance',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Openning Balance Amount",                
                "class": "form-control form-control-sm",
                "oninput": "digitsep(this)",
                "id": "openBal",
                "min" : "0"
              
            })
        )  
    closing_bal = forms.DecimalField(
        required=True,
        label='Closing Balance',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Closing Balance Amount ",                
                "class": "form-control form-control-sm",
                "oninput": "digitsep(this)",
                "id": "closeBal",
                "min" : "0"
              
            })
        )  
    # total_collections = forms.DecimalField(
    #     required=True,
    #     label='Collections',         
    #     widget=forms.HiddenInput(attrs={
    #             "placeholder": "Enter collections",                
    #             "class": "form-control form-control-sm",
    #             "oninput": "digitsep(this)",
    #             "id": "collections",
    #             "min" : "0"
              
    #         })
    #     )  
    total_processing_fees = forms.DecimalField(
        required=True,
        label='Processing Fees ',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Processing Amount",                
                "class": "form-control form-control-sm",
                "oninput": "digitsep(this)",
                "id": "processFees",
                "min" : "0"
              
            })
        )  
    # total_disbursed = forms.DecimalField(
    #     required=True,
    #     label='Disburement',         
    #     widget=forms.HiddenInput(attrs={
    #             "placeholder": "Enter ",                
    #             "class": "form-control form-control-sm",
    #             "oninput": "digitsep(this)",
    #             "id": "disbursed",
    #             "min" : "0"
              
    #         })
    #     )  
    injection_in = forms.DecimalField(
        required=True,
        label='Injection In',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Injection In Amount",                
                "class": "form-control form-control-sm",
                "oninput": "digitsep(this)",
                "id": "injectionIn",
                "value": 0,
                "min" : "0"
              
            })
        )  
    injection_out =forms.DecimalField(
        required=True,
        label='Injection Out',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Injection Out Amount",                
                "class": "form-control form-control-sm",
                "oninput": "digitsep(this)",
                "id": "injectionOut",
                "value": 0,
                "min" : "0"
              
            })
        )  
    total_banked = forms.DecimalField(
        required=True,
        label='Banked',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Banked Amount",                
                "class": "form-control form-control-sm",
                "oninput": "digitsep(this)",
                "id": "banked",
                "min" : "0"
              
            })
        )  
    total_expenses_daily = forms.DecimalField(
        required=True,
        label='Expenses',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Expenses Amount",                
                "class": "form-control form-control-sm",
                "oninput": "digitsep(this)",
                "id": "expenses",
                "min" : "0"
              
            })
        )  
    previous_closing_portfolio =forms.DecimalField(
        required=True,
        label='Closing Portfolio',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Closing Portfolio Amount",                
                "class": "form-control form-control-sm",
                "oninput": "digitsep(this)",
                "id": "closePortfolio",
                "min" : "0"
              
            })
        )  
    # total_clients_disbursed =  forms.IntegerField(
    #     label='Clients Disbursed',    
    #     widget=forms.NumberInput(attrs={
    #             "placeholder": "Enter Total Number of Cilents",                
    #             "class": "form-control form-control-sm",              
    #             "id":"clientsDisbursed",
    #             "min" : "0"            
    #         }))
    
    
    class Meta:
        model = Daily_Report
        fields = (
             'opening_bal'
            ,'total_processing_fees'
            ,'injection_in'
            ,'injection_out'
            ,'total_banked'
            ,'total_expenses_daily'
            ,'closing_bal'
            ,'previous_closing_portfolio'
            ,'activity_date'
        )
        widgets = {
            'activity_date': DateInput(attrs={'type': 'date','class': 'form-control form-control-sm'}),
        }
    