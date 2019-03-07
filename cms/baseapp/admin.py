from django.contrib import admin
from baseapp.models import *

# Register your models here.

admin.site.register(Incident)
admin.site.register(Report)
admin.site.register(Assistance)
admin.site.register(PublicSubcriber)
admin.site.register(GovernmentAgent)

