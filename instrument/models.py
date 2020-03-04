from django.db import models

# Create your models here.

#악기분류
class InstrumentClassification(models.Model):
    name = models.CharField(max_length=100)

#악기
class Instrument(models.Model):
    classification = models.ForeignKey(InstrumentClassification, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)