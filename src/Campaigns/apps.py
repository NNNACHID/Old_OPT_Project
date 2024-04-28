from django.apps import AppConfig


class CampaignsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Campaigns'

    def ready(self):
        import Campaigns.signals
