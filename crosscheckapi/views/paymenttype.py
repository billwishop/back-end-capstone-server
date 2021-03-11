"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from crosscheckapi.models import PaymentType

class PaymentTypes(ViewSet):
    """ Cross Check PaymentTypes """

    def list(self, request):
        """Handle GET requests to payment_type resource
        Returns:
            Response -- JSON serialized list of payment_types
        """
        payment_types = PaymentType.objects.all()

        serializer = PaymentTypeSerializer(
            payment_types, many=True, context={'request': request})

        return Response(serializer.data)

class PaymentTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for payment_types"""
    class Meta:
        model = PaymentType
        fields = ('id', 'label')