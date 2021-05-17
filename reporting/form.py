from django import forms
import datetime
from app.models import Branch

class Daily_report_search(forms.Form):    
    from_date = forms.DateField(
        initial=datetime.date.today,
        label='From Date', 
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class":"form-control form-control-sm"}
            )
        )
    to_date = forms.DateField(
        label='To Date', 
        initial=datetime.date.today,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class":"form-control form-control-sm"}
            )
        )
    
    branch = forms.CharField(        
        label='Select Branch', 
        required=False,
        max_length=50,
        widget=forms.Select(
            attrs={"class": "form-control form-control-sm", "id": "branchSelector"}, 
            choices=[(b.id, b.branch_name) for b in Branch.objects.all()]
            ),
    )