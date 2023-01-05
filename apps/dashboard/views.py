from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse

from hsutilities import domains as hsdomains
from hsutilities import users as hsusers

def get_param(request, name, default):
    if len(request.GET) > 0 and name in request.GET:
        return request.GET[name]
    if len(request.POST) > 0 and name in request.POST:
        return request.POST[name]
    return default


@login_required
def home(request):
    return render(request, 'dashboard.html', {})


@login_required
def search_command(request):
    searchtxt = get_param(request, 'searchtext', '')

    commands = {}

    for app in apps.get_app_configs():
        try:
            commands.update(app.get_commands())
        except AttributeError:
            None

    # make the keywords lowercase
    for c in commands:
        commands[c]['keywords'] = commands[c]['keywords'].lower()

    split_colon = searchtxt.split(':')
    search_strings = split_colon[0].lower().split(' ')

    # find all commands that are matched by at least one word
    found = {}
    for c in commands:
        for s in search_strings:
            if s in commands[c]['keywords']:
                found[c] = 1
    # drop all commands that are not matched by at least one word
    result = {}
    for f in found:
        add = f
        for s in search_strings:
            if not s in commands[f]['keywords']:
                add = None
        if add:
            result[add] = commands[add]

    pac = hsusers.get_current_pac()
    domains = hsdomains.get_domains_of_pac(pac)
    if len(result) == 1 and 'SelectDomain' in commands[list(result.keys())[0]]['keywords'] and len(split_colon) > 1:
        result['domains'] = {}
        for d in domains:
            if split_colon[1].strip().lower() in d:
                result['domains'][d] = 1

    return JsonResponse(result)

