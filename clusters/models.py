from django.db import models
from app.models import Branch
from django.contrib.auth.models import User

# Create your models here.
class Clusters(models.Model):
    id = models.BigAutoField(primary_key=True)
    cluster_name = models.CharField(max_length=100, unique=True)
              
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=False)
    update_on = models.DateTimeField(null=True)
    updated_by = models.IntegerField(default=False, null=True)
    
    
class Cluster_branches(models.Model):
    id = models.BigAutoField(primary_key=True)
    cluster_id = models.ForeignKey(Clusters, on_delete=models.CASCADE)
    branch_id = models.ForeignKey(Branch, on_delete=models.CASCADE)
    
    
class Assignments(models.Model):
    id = models.BigAutoField(primary_key=True)
    cluster_id = models.ForeignKey(Clusters, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)               
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(default=False)
    update_on = models.DateTimeField(null=True)
    updated_by = models.IntegerField(default=False, null=True)
    
