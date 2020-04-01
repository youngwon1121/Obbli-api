from django.contrib import admin
from .models import Instrument, InstrumentClassification

# Register your models here.
admin.site.register(InstrumentClassification)
admin.site.register(Instrument)