
from django import forms
from app.models import Branch
from django.contrib.auth.models import User
from django.contrib.postgres.forms import SimpleArrayField
from app.functions import get_branch_supervisors
from app.models import Profile

class ClusterAddForm(forms.Form):
    cluster_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Cluster Name",                
                "class": "form-control form-control-sm",
                "value": ""
            }
        ))
   
BRANCHES = ((b.id, b.branch_name) for b in Branch.objects.all())
SUPAS = [(u.id, u.username) for u in User.objects.filter(groups__in=[2,4])]#get_branch_supervisors()

class AddBranchesToCluster(forms.Form):    
    
    branches = forms.MultipleChoiceField(
    required=False,
    widget=forms.SelectMultiple(attrs={
    "class": "select2 form-control form-control-sm",
    "multiple": "multiple", 
    "style": "{height: 36px; width: 100%;}" 
    }),choices=BRANCHES)
   
    
class AddSupervisorToCluster(forms.Form):
    supervisor = forms.CharField(  
                                 required=False,      
        label='Select Supervisor',        
        max_length=50,
        widget=forms.Select(
            attrs={"class": "form-control form-control-sm" }, 
            choices=SUPAS
            ),
    )

class BranchAddClusterForm(forms.Form):
    
    branch = forms.CharField(        
        label='Select Branch',        
        max_length=50,
        widget=forms.Select(
            attrs={"class": "form-control form-control-sm" }, 
            choices=[(b.id, b.branch_name) for b in Branch.objects.all()]
            ),
    )
    