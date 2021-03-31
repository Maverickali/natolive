from django.db import models
from app.models import Potential_Customers, Branch

# Create your models here.
class Ids(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_number = models.CharField(max_length=100, null=True)
    id_status = models.CharField(default='submitted', max_length=100)
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    id_loan_count = models.IntegerField(default=False, null=True)
    customer_id = models.ForeignKey(Potential_Customers, on_delete=models.CASCADE)
    branch_id_holder = models.IntegerField(default=1)
    id_override_status = models.CharField(default='no', max_length=50)
    id_override_reason = models.CharField(default=False , max_length=200)
    resubmission_date = models.DateField(default=False, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=False)
    update_on = models.DateTimeField(auto_now=True, null=True)
    updated_by = models.IntegerField(default=False, null=True)
    

        