from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from hsutilities import users as hsusers
from hsutilities import domains as hsdomains

import os, json


def get_wordpress_installation_in_path(user, domain, path):
    version_file = "wp-includes/version.php"
    cmd = f'if [ -f {path}/{version_file} ]; then cat {path}/{version_file} | grep "wp_version = "; fi'
    cmd = cmd.replace('"', '\\"')
    stream = os.popen(f'sudo -u {user} -s /bin/bash -c "{cmd}"')
    version = stream.read().strip()
    if version:
        return {'user': user, 'domain': domain, 'path': path, 'version': version.split('=')[1].strip(" ;'")}
    return None


def get_wordpress_installations_of_user(user):

    installations = []
    domains = hsdomains.get_domains_of_user(user)

    for domain in (domains or []):
        installation = get_wordpress_installation_in_path(user, domain, f'~/doms/{domain}/htdocs-ssl')
        if installation:
            installations.append(installation)

        subdomains = hsdomains.get_subdomains_of_domain(user, domain)
        for subdomain in (subdomains or []):
            installation = get_wordpress_installation_in_path(user, f'{subdomain}.{domain}', f'~/doms/{domain}/subs-ssl/{subdomain}')
            if installation:
                installations.append(installation)

    return installations


def get_wordpress_installations_of_pac(pac):

    result = []
    installations = get_wordpress_installations_of_user(pac)
    if installations:
        result += installations
    users = hsusers.get_users_of_pac(pac)
    for user in (users or []):
        installations = get_wordpress_installations_of_user(f"{pac}-{user}")
        if installations:
            result += installations
    return result


@login_required
def wordpress_list(request):
    pac = hsusers.get_current_pac()
    table = get_wordpress_installations_of_pac(pac)
    return render(request, 'webapp_list.html', {
            'webapp': 'WordPress',
            'captions': json.dumps(['User', 'Domain', 'WordPress Version']),
            'data': json.dumps(table)})
