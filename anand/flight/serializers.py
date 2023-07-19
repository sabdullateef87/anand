from rest_framework import serializers
from .models import FlightPriceConfig

class FlightConfigSerilizer(serializers.ModelSerializer):
    class Meta:
        model = FlightPriceConfig
        fields = ['current_flight_time', 'next_flight_time', 'flight_category', 'price', 'starting_point', 'destination', 'is_available', 'number_of_seats', 'available_seats']
    def validate(self, data):
        pass