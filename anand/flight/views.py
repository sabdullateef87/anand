from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .manager import FlightManager
from .serializers import FlightConfigSerilizer
# Create your views here.

class CreateFlight(APIView, FlightManager):
    def post(self, request):
        request_body = request.data
        serializer = FlightConfigSerilizer(data=request_body)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

class SearchAvailableFlight(APIView, FlightManager):
    pass
