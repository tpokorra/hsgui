from django.apps import AppConfig


class NextcloudConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.nextcloud'

    def get_commands(self):
        commands = {}
        commands["Neue Nextcloud einrichten"] = {'keywords': "Nextcloud,Neue,Neu,anlegen,hinzufügen,füge,hinzu,lege,an"}
        return commands
