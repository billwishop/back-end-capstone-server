"""View module for handling requests about properties"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from crosscheckapi.models import Property, Landlord, Payment, PaymentType, TenantPropertyRel

class Properties(ViewSet):
    """Cross Check Properties"""

    def create(self, request):
        """Handle POST operations for properties
        Returns:
            Response -- JSON serialized property instance
        """
        # landlord = authenticated user
        landlord = Landlord.objects.get(user=request.auth.user)

        rental = Property()
        rental.street = request.data["street"]
        rental.city = request.data["city"]
        rental.state = request.data["state"]
        rental.postal_code = request.data["postal_code"]
        rental.landlord = landlord

        rental.save()

        serializer = PropertySerializer(
            rental, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PropertySerializer(serializers.ModelSerializer):
    """JSON serializer for properties"""
    class Meta:
        model = Property
        fields = ('id', 'street', 'city', 
        'state', 'postal_code', 'landlord')
