from django.db.models import Q

class FlightManager:
    def get_flight_by_id(self, id):
        pass

    def filter_flight(self, queryset, flight_category, starting_point, destination):
        return queryset.objects.filter(flight_category=flight_category, starting_point=starting_point, destination=destination)
        
