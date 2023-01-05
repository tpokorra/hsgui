from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from apps.domains.forms import DomainsAddForm
from hsutilities import users as hsusers
from hsutilities import admin as hsadmin


def get_domain_options():
    domainoptions = []
    domainoptions.append(
        {'name': 'greylisting',
        'label': "E-Mails werden verzögert durch den Mailserver angenommen, siehe Greylisting. Ist die Option deaktiviert, werden E-Mails ohne Verzögerung angenommen."})
    domainoptions.append(
        {'name': 'multiviews',
        'label': "Der Webserver berücksichtigt Einstellungen im Browser beim Abruf einer Domain (z.B. eine bevorzugte Sprache). Die Option kann mit einer .htaccess-Datei für jedes Verzeichnis konfiguriert werden."})
    domainoptions.append(
        {'name': 'indexes',
        'label': "Der Webserver erzeugt für Verzeichnisse, die keine eigene Index-Datei enthalten, eine Liste mit den im Verzeichnis enthaltenen Dateien. Ist die Option deaktiviert, wird ein Fehler 303 ausgegeben. Die Option kann mit einer .htaccess-Datei für jedes Verzeichnis konfiguriert werden."})
    domainoptions.append(
        {'name': 'htdocsfallback',
        'label': "Der Webserver leitet auf die Hauptdomain, wenn keine Sub-Domain angelegt ist. Ist die Option deaktiviert, wird ein Fehler 404 ausgegeben: Seite nicht gefunden."})
    domainoptions.append(
        {'name': 'includes',
        'label': "Der Webserver erkennt SSI-Komandos und -Dateien. Die Option kann mit einer .htaccess-Datei für jedes Verzeichnis konfiguriert werden."})
    domainoptions.append(
        {'name': 'backupmxforexternalmx',
        'label': "Der Paket-Hive wird als Weiterleitung (transport) beim Mail-In-Server eingetragen. Ist die Option aktiv, ist der Hostsharing-Mail-In-Server Backup-MX. Der eigentliche Mailserver befindet sich außerhalb der Infrastruktur von Hostsharing (z.B. anderer Provider, DSL-Anschluss mit fester IP)"})
    domainoptions.append(
        {'name': 'letsencrypt',
        'label': "Es wird automatisch ein TLS Zertifikat für diese Domain und alle im Feld „validsubdomainnames” angegebenen Subdomains erzeugt"})
    domainoptions.append(
        {'name': 'autoconfig',
        'label': 'Eine Unterstützung für die Konfiguration von E-Mail-Programmen durch die Verfahren "Autoconfig" (Mozilla) und "Autodiscover" (Microsoft) wird für die Domain eingeschaltet'})
    return domainoptions


@login_required
def domains_add(request):

    if request.method == "GET":
        return render(request, 'domain_add.html', {})

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
                return render(request, 'domain_add.html', {'domain': domain, 'owner': owner, 'errors': e})

            return redirect(f'/domains/show/{domain}')
        else:
            return render(request, 'domain_add.html', {'domain': domain, 'owner': owner, 'errors': form.errors.values()})


@login_required
def domains_show(request, domain):
    pac = hsusers.get_current_pac()
    api = hsadmin.get_api(username=pac)
    domain = api.domain.search(where = {'name': domain})

    if len(domain) == 1:
        domain = domain[0]
        return render(request, 'domain_show.html', {'domain': domain, 'domainoptions': get_domain_options()})

    return redirect("/")


@login_required
def domains_edit(request, domain):
    pac = hsusers.get_current_pac()
    api = hsadmin.get_api(username=pac)
    domainname = domain
    domain = api.domain.search(where = {'name': domainname})

    if len(domain) != 1:
        return redirect('/')

    domain = domain[0]
    if request.method == "GET":
        return render(request, 'domain_edit.html', {'domain': domain, 'domainoptions': get_domain_options()})
    elif request.method == "POST":
        options = get_domain_options()
        new_options = []
        for option in options:
            if option['name'] in request.POST and request.POST[option['name']] == "1":
                new_options.append(option['name'])

        try:
            api.domain.update(where = {'name': domainname}, set = {'domainoptions': new_options})
        except Exception as e:
            return render(request, 'domain_edit.html', {'domain': domain, 'domainoptions': get_domain_options(), 'errors': e})
        return redirect(f'/domains/show/{domainname}')


@login_required
def domains_delete(request, domain):
    pac = hsusers.get_current_pac()
    api = hsadmin.get_api(username=pac)
    domainname = domain
    domain = api.domain.search(where = {'name': domainname})

    if len(domain) != 1:
        return redirect("/")

    domain = domain[0]
    if request.method == "GET":
        return render(request, 'domain_show.html', {'domain': domain, 'domainoptions': get_domain_options(), 'action': 'delete'})
    elif request.method == "POST":
        api.domain.delete(where = {'name': domainname})
        return redirect('/')


