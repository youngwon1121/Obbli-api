from django.test import TestCase
from .models import Instrment, InstrumentClassification
# Create your tests here.

def create_instrument_classification():
    instrument_classification = InstrumentClassification.objects.create(name='ETC')
    return instrument_classification

def create_instrument(instrument_classification):
    violin = Instrument.objects.create(
        classification = instrument_classification.id,
        name = 'Violin'
    )
    return violin

class InstrumentModelTests(TestCase):

    def test_delete_instrument_classification(self):
        etc = create_instrument_classification()
        violin = create_instrument(etc) 
        etc.delete()