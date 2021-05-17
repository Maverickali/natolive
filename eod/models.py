from django.db import models
from app.models import Branch
from django.contrib.auth.models import User

# Create your models here.
class Eod(models.Model):
    id = models.BigAutoField(primary_key=True)
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    is_closed = models.BooleanField(default=False)
    closed_on = models.DateTimeField(null=True)
    closed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    days_collections = models.FloatField(default=0.0, null=True)           
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=False)
    update_on = models.DateTimeField(null=True)
    updated_by = models.IntegerField(default=False, null=True)
    
