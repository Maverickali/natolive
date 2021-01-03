from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate
from app.forms import SearchForm, TreasuryForm
import re

def group_required(request, *group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(user):
        if request.user.is_authenticated():
            if bool(user.groups.filter(name__in=group_names)) | user.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url='/login/')

def branch_disable(user_name,form):
    res = re.split('\d*\D+',user_name)
    if form == 'search':
        form = SearchForm(initial={'branch_name': str(res[1])}, auto_id=False)
    else:
        form = TreasuryForm(initial={'branch_name': str(res[1])}, auto_id=False)
    if len(str(res[1])) != 0:
        form.fields['branch_name'].disabled = True
        # _form.fields['branch_name'].disabled = True
    return form