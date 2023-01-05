from django.apps import AppConfig


class DomainsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.domains'

    def get_commands(self):
        commands = {}
        commands["Bearbeite Domain"] = {'keywords': "Domain,Bearbeiten,Bearbeite,SelectDomain"}
        commands["Lösche Domain"] = {'keywords': "Domain,Löschen,Lösche,Entfernen,Entferne,SelectDomain"}
        commands["Neue Domain hinzufügen"] = {'keywords': "Domain,Neue,Neu,anlegen,hinzufügen,füge,hinzu,lege,an", 'url': '/domains/add'}
        commands["Greylisting abschalten"] = {'keywords': "Domain,Greylisting,grey,listing,abschalten,schalte,ab,SPAM,SelectDomain"}
        return commands

