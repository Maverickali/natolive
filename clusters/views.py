from django.shortcuts import render
from app.functions import get_user_group, get_branch_id
from app.models import Branch
from .models import Clusters
from .forms import ClusterAddForm , AddBranchesToCluster, AddSupervisorToCluster
from clusters.models import Assignments, Cluster_branches
from clusters.forms import BranchAddClusterForm
from django.contrib.auth.models import User

def manage_cluster(request):
    msg = None
    msg_status = None
    success = False
    form = None
    active = 'cluster'
    frmCluster = ClusterAddForm()
    frmBranch = AddBranchesToCluster()
    frmSupervisor = AddSupervisorToCluster()
    # branch = Branch.objects.get(id=get_branch_id(request))
    activity_data = Clusters.objects.all()
    # select_related().filter() 
    # Clusters.objects.all()#filter(branch_id=get_branch_id(request))    
    # txn_date = get_Open_Txn_date(request)
   
    if request.method == 'POST' and request.POST:
        frmCluster = ClusterAddForm(request.POST)
        if frmCluster.is_valid():
            cluster_name = frmCluster.cleaned_data.get('cluster_name')
            if cluster_name != '':
                cluster = Clusters.objects.get_or_create(cluster_name=cluster_name,created_by=request.user.id)
                if cluster:
                    msg = "Cluster Successfully Created"
                    msg_status = True
                else:
                    msg = "Cluster Already Exists"
                    msg_status = False 
        #  Assigning Branches to Cluster               
        frmBranch = AddBranchesToCluster(request.POST)
        if frmBranch.is_valid():
            branches = frmBranch.cleaned_data.get('branches')
            cluster_id = request.POST.get('id',False)
            cluster = Clusters.objects.get(id=cluster_id)
            for branch in branches:
                branch_instance = Branch.objects.get(id=branch)
                B = Cluster_branches.objects.update_or_create(cluster_id=cluster, branch_id=branch_instance)               
                
            msg = 'The Selected Branches have been assign to cluster'
            msg_status = True
        frmSupervisor = AddSupervisorToCluster(request.POST)
        if frmSupervisor.is_valid():
            supervisors = frmSupervisor.cleaned_data.get('supervisor')
            cluster_id = request.POST.get('id',False)
            cluster = Clusters.objects.get(id=cluster_id)
            for supa in supervisors:
                user_instance = User.objects.get(id=supa)
                assignment = Assignments.objects.update_or_create(
                    cluster_id=cluster, 
                    user_id=user_instance, 
                    created_by=request.user.id)
            msg= 'The Supervisor Assigned has been assigned cluster'
            msg_status=True
                           
               
    context = {
        'activity_data':activity_data,
        'frmCluster':frmCluster,
        'frmBranch':frmBranch,
        'frmSupervisor':frmSupervisor, 
        'branchs' : Branch.objects.all(),       
        # 'txn_date': txn_date,
        "msg": msg, 
        'msg_status': msg_status ,
        "success": success,
        "currentGroup": get_user_group(request), 
        'active':active}

    return render(request, 'cluster/create_cluster.html', context)

    

def view_cluster(request):
    pass

def add_branch_cluster(request):
    msg = None
    msg_status = None
    success = False
    form = None
    active = 'cluster'
    form = BranchAddClusterForm()
    #branch = Branch.objects.get(id=get_branch_id(request))
    activity_data = Clusters.objects.all()#filter(branch_id=get_branch_id(request))    
    # txn_date = get_Open_Txn_date(request)
    if request.method == 'POST' and request.POST:
        cluster_id = request.POST.get('id', False)
        branch_id = request.POST.get('branch', False)
        branch = Branch.objects.get(id=branch_id)
        cluster = Cluster_branches.objects.get_or_create(cluster_id=cluster_id,branch_id=branch)
        if cluster:
            msg = "Branch Successfully Added to Cluster"
            msg_status = True
        else:
            msg = "Cant assign Branch to cluster"
            msg_status = False
      
    context = {
        'activity_data':activity_data,
        'form':form,
        # 'txn_date': txn_date,
        "msg": msg, 
        'msg_status': msg_status ,
        "success": success,
        "currentGroup": get_user_group(request), 
        'active':active}

    return render(request, 'cluster/create_cluster.html', context)
