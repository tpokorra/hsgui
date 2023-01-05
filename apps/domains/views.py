from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.domains.forms import DomainsAddForm
from hsutilities import users as hsusers
from hsutilities import admin as hsadmin

@login_required
def domains_add(request):

    if request.method == "GET":
        return render(request, 'domains_add.html', {})

    elif request.method == "POST":
        form = DomainsAddForm(request.POST)
        domain = form.data.get('domain')
        owner = form.data.get('owner')
        if form.is_valid():

            pac = hsusers.get_current_pac()
            api = hsadmin.get_api(username=pac)

            try:
                api.domain.add(set = {'name': domain, 'user': owner})
            except Exception as e:
                return render(request, 'domains_add.html', {'domain': domain, 'owner': owner, 'errors': e})

            return redirect(f'/domains/show/{domain}')
        else:
            return render(request, 'domains_add.html', {'domain': domain, 'owner': owner, 'errors': form.errors.values()})
