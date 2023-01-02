from django.apps import AppConfig


class WordpressConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.wordpress'

    def get_commands(self):
        commands = {}
        commands["Wordpress Installationen auflisten"] = {'keywords': "Wordpress,Installationen,auflisten,liste,auf,anzeigen,zeige,an", "url": "/wordpress/list"}
        return commands
