from django.contrib import admin
from .models import ExternalLedger, Entity

admin.site.register(ExternalLedger)
admin.site.register(Entity)
