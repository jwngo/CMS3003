from django.apps import AppConfig
from .APImodules import StatusReportAPIManager, NotificationManager
from django.conf import settings

class BaseappConfig(AppConfig):
    name = 'baseapp'

    def ready(self):   
        StatusReportAPIManager.start()
        NotificationManager.start()
        