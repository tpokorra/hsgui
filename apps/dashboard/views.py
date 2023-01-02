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
    commands["Bearbeite Domain"] = {'keywords': "Domain,Bearbeiten,Bearbeite"}
    commands["Lösche Domain"] = {'keywords': "Domain,Löschen,Lösche,Entfernen,Entferne"}
    commands["Neue Domain hinzufügen"] = {'keywords': "Domain,Neue,Neu,anlegen,hinzufügen,füge,hinzu,lege,an"}
    commands["Wordpress Installationen auflisten"] = {'keywords': "Wordpress,Installationen,auflisten,liste,auf,anzeigen,zeige,an", "url": "/wordpress/list"}
    commands["Neue Nextcloud einrichten"] = {'keywords': "Nextcloud,Neue,Neu,anlegen,hinzufügen,füge,hinzu,lege,an"}
    commands["Greylisting abschalten"] = {'keywords': "Domain,Greylisting,grey,listing,abschalten,schalte,ab,SPAM"}

    split_colon = searchtxt.split(':')
    search_strings = split_colon[0].split(' ')

    # find all commands that are matched by at least one word
    found = {}
    for c in commands:
        for s in search_strings:
            if s.lower() in commands[c]['keywords'].lower():
                found[c] = 1
    # drop all commands that are not matched by at least one word
    result = {}
    for f in found:
        add = f
        for s in search_strings:
            if not s.lower() in commands[f]['keywords'].lower():
                add = None
        if add:
            result[add] = commands[add]

    domains = {'testdomain.de', 'example.org', 'beispielverein.de'}
    pac = hsusers.get_current_pac()
    domains = hsdomains.get_domains_of_pac(pac)
    if len(result) == 1 and 'Domain' in commands[list(result.keys())[0]]['keywords'] and len(split_colon) > 1:
        result['domains'] = {}
        for d in domains:
            if split_colon[1].strip().lower() in d:
                result['domains'][d] = 1

    return JsonResponse(result)

