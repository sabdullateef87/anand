from django.contrib import admin
from .models import FlightPriceConfig, SourceModel, DestinationModel
# Register your models here.
admin.site.register(FlightPriceConfig)
admin.site.register(SourceModel)
admin.site.register(DestinationModel)