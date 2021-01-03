from django import forms
from .models import Injections
import datetime
from app.models import Branch


TITLE_CHOICES = [
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
]

class SearchForm(forms.Form):    
    from_date = forms.DateField(
        initial=datetime.date.today,
        label='From Date', 
        widget=forms.SelectDateWidget(

            attrs={"class":"form-control form-control-sm"}
            )
        )
    to_date = forms.DateField(
        label='To Date', 
        initial=datetime.date.today,
        widget=forms.SelectDateWidget(
            attrs={"class": "form-control form-control-sm"}
            )
        )
    inj_status = forms.BooleanField(
        initial=True,
        required=False,
        label='Pending Injections', 
        widget=forms.CheckboxInput(
           attrs={
               "class": "form-check-input",     
               "style": "margin-left: 50px;"
               }
        )
    )
    all_branchs = forms.BooleanField(       
        required=False,
        label='All Branches', 
        widget=forms.CheckboxInput(
           attrs={
               "class": "form-check-input",
               "id": "allBranches",     
               "style": "margin-left: 50px;"
               }
        )
    )
    branch_name = forms.CharField(        
        label='Select Branch', 
        required=False,
        max_length=50,
        widget=forms.Select(
            attrs={"class": "form-control form-control-sm", "id": "branchSelector"}, 
            choices=[(b.id, b.branch_name) for b in Branch.objects.all()]
            ),
    )
    
# (b.branch_name) for b in Branch.objects.select_related().get(record_id = id)
class TreasuryForm(forms.ModelForm):
    branch_name = forms.CharField(        
        label='Select Branch', 
        max_length=50,
        widget=forms.Select(attrs={"class": "form-control"}, choices=[(b.id, b.branch_name) for b in Branch.objects.all()]),
    )    
    new_customer_numbers = forms.IntegerField(
        label='# New Customer(s)',         
        widget=forms.NumberInput(attrs={
                "placeholder": "Enter Number of New Customer Disbursed",                
                "class": "form-control",
                "oninput": "subTotalCustomers(this)",
                "value": 0,
                "id":"newcustomer",
                "min" : "0"
            })
        )
    repeat_customer_numbers = forms.IntegerField(
        label='# Repeat Customer(s)',         
        widget=forms.NumberInput(attrs={
                "placeholder": "Enter Number of New Customer Disbursed",                
                "class": "form-control",
                "oninput": "subTotalCustomers(this)",
                "value": 0,
                "id":"repeatcustomer",
                "min" : "0"
                
            })
        )
    new_customer_amount = forms.DecimalField(
        label='Disbursed Amount to New Customer(s)',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Disbursed Amount to New Customer(s)",                
                "class": "form-control",               
                "oninput": "format(this)",
                "id": "newCustomerAmount",
                "min" : "0"
            })
        )
    repeat_customer_amount = forms.DecimalField(
        label='Disbursed Amount to Repeat Customer(s)',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Disbursed Amount to Repeat Customer(s)",                
                "class": "form-control",
                "oninput": "format(this)",
                "id": "repeatCustomerAmount",
                "min" : "0"
            })
        )
    injection_amount = forms.DecimalField(
        required=False,
        label='Injection Amount',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Injection Amount ",                
                "class": "form-control",
                "onkeyup": "format(this)",
                "id": "injectionAmount",
                "disabled": True,
                "min" : "0"
            })
        )
    cash_forward = forms.DecimalField(
        required=False,
        label='Cash Forward',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Cash Forward Need)",                
                "class": "form-control",
                "onkeyup": "format(this)",
                "id": "cashForward",
                "min" : "0"
            })
        )
    injection_status = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
           attrs={
               "class": "form-check-input", 
               "id": "injection_status", 
               "onclick": "enableInjectionAmount()" }
        )
    )
    date = forms.DateField(
        initial=datetime.date.today,
        widget=forms.SelectDateWidget(
            attrs={"class":"form-control"}
            )
        )
    cash_reserve_need = forms.CharField( required=False,
            widget=forms.HiddenInput(attrs={
                    "placeholder": "Created by",                
                    "class": "form-control"
                
                })
        )
    created_by = forms.CharField( required=False,
        widget=forms.HiddenInput(attrs={
                "placeholder": "Created by",                
                "class": "form-control"               
            })
    )
    
    class Meta:
        model = Injections
        fields = (
            'branch_name', 
            'new_customer_numbers', 
            'repeat_customer_numbers', 
            'new_customer_amount',
            'repeat_customer_amount',
            'injection_amount',
            'cash_forward',
            'injection_status',
            'date',
            'cash_reserve_need',
            'created_by'
            )