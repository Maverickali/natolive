from django import forms
from .models import Injections
import datetime
from app.models import Branch, Profile, RM_Daily_Activity, RM_Weekly_Customers, RM_Weekly_Customers_Portfolio, Targets_Collections_Disbursement, Targets_Portfoilo
from django.forms.widgets import DateInput
from django.contrib.auth.models import User



TITLE_CHOICES = [
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
]

TIER_DAYS = [
    ('active', 'Active Portfolio'),
    ('1-30', '1 - 30 Days'),
    ('31-60', '31 - 30 Days'),
    ('60+', 'Above 60'),
] 

CUSTOMER_CATEGORIES = [
    ('active', 'Active Customers'),
    ('new', 'New Customers'),
    ('1-30', '1 - 30 Days'),
    ('31-60', '31 - 30 Days'),
    ('60+', 'Above 60'),
] 

customer_category =  forms.CharField(        
        label='Select Customer Category',       
        required=False,
        max_length=50,
        widget=forms.Select(
            attrs={"class": "form-control form-control-sm" }, 
            choices=CUSTOMER_CATEGORIES
            ),
    ) 

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['branch_id', 'location']
        widgets = {
            'creationdate': DateInput(attrs={'type': 'date'}),
        }


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
               "min" : "0","onclick":"empty(this)" 
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
               "min" : "0","onclick":"empty(this)" 
                
            })
        )
    new_customer_amount = forms.DecimalField(
        label='Disbursed Amount to New Customer(s)',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Disbursed Amount to New Customer(s)",                
                "class": "form-control",               
                "oninput": "format(this)",
                "id": "newCustomerAmount",
               "min" : "0","onclick":"empty(this)" 
            })
        )
    repeat_customer_amount = forms.DecimalField(
        label='Disbursed Amount to Repeat Customer(s)',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Disbursed Amount to Repeat Customer(s)",                
                "class": "form-control",
                "oninput": "format(this)",
                "id": "repeatCustomerAmount",
               "min" : "0","onclick":"empty(this)" 
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
               "min" : "0","onclick":"empty(this)" 
            })
        )
    cash_forward = forms.DecimalField(
        required=False,
        label='Cash Forward',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Cash Forward Need",                
                "class": "form-control",
                "onkeyup": "format(this)",
                "id": "cashForward",
               "min" : "0","onclick":"empty(this)" 
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

class RmDailyActivityForm(forms.ModelForm):
    new_cilents = forms.IntegerField(
        label='Number of New Customers',    
        widget=forms.NumberInput(attrs={
                "placeholder": "Enter Total Number of New Customer",                
                "class": "form-control form-control-sm",              
                "value": 0,
                "id":"new_cilents",
               "min" : "0","onclick":"empty(this)"               
            }))
    cilents_collected = forms.IntegerField(
        label='Number of Customers Collected From',    
        widget=forms.NumberInput(attrs={
                "placeholder": "Enter Number of New Customer Collected",                
                "class": "form-control form-control-sm",
                "value": 0,
                "id":"cilents_collected",
               "min" : "0","onclick":"empty(this)" 
                
            }))
    amount_collected = forms.DecimalField(
        required=False,
        label='Amount Collected',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Amount Collected",                
                "class": "form-control form-control-sm",
                "onkeyup": "digitsep(this)",
                "id": "amount_collected",
               "min" : "0","onclick":"empty(this)" ,
                "value": 0.0
            })
        )
    amount_disbursed = forms.DecimalField(
        required=False,
        label='Amount Disbursed',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Amount Disbursed",                
                "class": "form-control form-control-sm",
                "onkeyup": "digitsep(this)",
                "id": "amount_disbursed",
               "min" : "0","onclick":"empty(this)" ,
                "value": 0.0
            })
        )
    activitydate = forms.DateField(
        label='Activity Date', 
        initial=datetime.date.today,
        widget=forms.SelectDateWidget(
            attrs={"class":"form-control form-control-sm"}
            )
        )
    class Meta:
        model = RM_Daily_Activity
        fields = (  'cilents_collected'
                    ,'amount_collected'
                    ,'new_cilents'
                    ,'amount_disbursed'
                    ,'activitydate'  )

class RMWeeklyCustomersPortfolioForm(forms.ModelForm):

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
    day_category = forms.CharField(        
        label='Select Days Category',       
        required=False,
        max_length=50,
        widget=forms.Select(
            attrs={"class": "form-control form-control-sm" }, 
            choices=TIER_DAYS
            ),
    )
       
    portfolio_clients = forms.IntegerField(
        label='Portfolio Clients',    
        widget=forms.NumberInput(attrs={
                "placeholder": "Enter Total Portfolio Clients",                
                "class": "form-control form-control-sm",              
                "value": 0,
                "id":"new_cilents",
               "min" : "0","onclick":"empty(this)"                 
            }))
    portfolio_amount = forms.DecimalField(
        required=False,
        label='Portfolio Amount',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Total Portfolio Amount",                
                "class": "form-control form-control-sm",
                "onkeyup": "digitsep(this)",
                "id": "portfolio_amount",
               "min" : "0","onclick":"empty(this)" 
            })
        )
       
    class Meta:
        model = RM_Weekly_Customers_Portfolio
        fields = ['day_category', 'from_date', 'to_date', 'portfolio_amount'
        , 'portfolio_clients'  ]
        
class SetTargetsForm(forms.ModelForm):

  
    collections = forms.DecimalField(
        required=True,
        label='Collections',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Total Target Collections Amount",                
                "class": "form-control form-control-sm",
                "onkeyup": "digitsep(this)",
                "id": "collections",
               "min" : "0","onclick":"empty(this)" 
            })
        )
    disbursements = forms.DecimalField(
        required=True,
        label='Disbursements',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Total Target Disbursements Amount",                
                "class": "form-control form-control-sm",
                "onkeyup": "digitsep(this)",
                "id": "disbursements",
               "min" : "0","onclick":"empty(this)" 
            })
        )
    active_portfoilo = forms.DecimalField(
        required=True,
        label='Active Portfoilo',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Active Portfoilo Amount",                
                "class": "form-control form-control-sm",
                "onkeyup": "digitsep(this)",
                "id": "active_portfoilo",
               "min" : "0","onclick":"empty(this)" 
            })
        )
    bad_portfoilo = forms.DecimalField(
        required=True,
        label='Bad Portfoilo',         
        widget=forms.TextInput(attrs={
                "placeholder": "Enter Bad Portfoilo Amount",                
                "class": "form-control form-control-sm",
                "onkeyup": "digitsep(this)",
                "id": "bad_portfoilo",
               "min" : "0","onclick":"empty(this)" 
            })
        )
    rm_id = forms.CharField(        
        label='Select RM', 
        required=True,
        max_length=50,
        widget=forms.Select(            
            attrs={"class": "form-control form-control-sm", "id": "rm"}, 
            choices=[
                (b.branch_id_id, b.user_id) for b in Profile.objects.all()
                ]
            
            ),
    )

    from_date = forms.DateField(
        required=True,
        initial=datetime.date.today,
        label='From Date', 
        widget=forms.SelectDateWidget(
                attrs={"class":"form-control form-control-sm"}
            )
        )
    to_date = forms.DateField(
        required=True,
        label='To Date', 
        initial=datetime.date.today,
        widget=forms.SelectDateWidget(
            attrs={"class": "form-control form-control-sm"}           
            )
        )
    new_customers =  forms.IntegerField(
        required=True,
        label='New Customer',    
        widget=forms.NumberInput(attrs={
                "placeholder": "Enter New Customers",                
                "class": "form-control form-control-sm",              
               "min" : "0","onclick":"empty(this)"                 
            }))
    

    class Meta:
        model = Targets_Collections_Disbursement
        fields = ['collections', 'new_customers' , 
        'disbursements', 'bad_portfoilo', 'active_portfoilo',
        'from_date','to_date', 'rm_id']

class TargetsPortfoiloForm(forms.ModelForm):

    day_category = forms.CharField(        
        label='Select Days Category',       
        required=False,
        max_length=50,
        widget=forms.Select(
            attrs={"class": "form-control form-control-sm" }, 
            choices=TIER_DAYS
            ),
    )
    class Meta:
        model = Targets_Portfoilo
        fields = [  'rm_id','day_category','number_cilents','from_date','to_date']



class RMWeeklyCustomersForm(forms.ModelForm):

    customer_category =  forms.CharField(        
        label='Select Customer Category',       
        required=False,
        max_length=50,
        widget=forms.Select(
            attrs={"class": "form-control form-control-sm" }, 
            choices=CUSTOMER_CATEGORIES
            ),
        )
    number_customers = forms.IntegerField(
        label='Number Of Customers',    
        widget=forms.NumberInput(attrs={
                "placeholder": "Enter Number Of Customers",                
                "class": "form-control form-control-sm",              
                "value": 0,
                "id":"number_customer",
               "min" : "0","onclick":"empty(this)"                 
            }))
    class Meta:
        model = RM_Weekly_Customers
        fields =  [  'number_customers','customer_category','from_date','to_date']


