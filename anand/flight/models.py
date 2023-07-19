from unicodedata import name
from django.db import models
from django.template.defaultfilters import truncatechars

# Create your models here.
class FlightPriceConfig(models.Model):
    FLIGHT_TYPE = (
        ('ECONOMY', 'ECONOMY'),
        ('PREMIUM_ECONOMY', 'PREMIUM_ECONOMY'),
        ('FIRST_CLASS', 'FIRST_CLASS'),
        ('BUSINESS_CLASS', 'BUSINESS_CLASS')
    )

    current_flight_time = models.DateField(null=False, blank=False)
    next_flight_time = models.DateField(null=False, blank=False)
    flight_category = models.CharField(max_length=255, null=False, blank=False, choices=FLIGHT_TYPE)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    starting_point = models.ForeignKey('SourceModel', on_delete=models.CASCADE, null=False, blank=False)
    destination = models.ForeignKey('DestinationModel', on_delete=models.CASCADE, null=False, blank=False)
    is_available = models.BooleanField(default=False)
    number_of_seats = models.IntegerField(default=0)
    available_seats = models.IntegerField(default=0)

    
    @property
    def flight_ref(self):
        prefix = self.starting_point
        suffix = self.destination
        return f'{prefix} to {suffix}'

    def __str__(self):
        return f'{self.flight_ref}'


class SourceModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, primary_key=True, unique=True)
    def __str__(self):
        return self.name

class DestinationModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, primary_key=True, unique=True)
    def __str__(self):
        return self.name


