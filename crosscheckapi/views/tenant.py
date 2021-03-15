"""View module for handling requests about tenants"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from crosscheckapi.models import Tenant, Landlord

class Tenants(ViewSet):
    """Cross Check tenants"""

    def create(self, request):
        """Handle POST operations for tenants
        Returns:
            Response -- JSON serialized tenant instance
        """
        landlord = Landlord.objects.get(user=request.auth.user)

        tenant = Tenant()
        tenant.phone_number = request.data["phone_number"]
        tenant.email = request.data["email"]
        tenant.first_name = request.data["first_name"]
        tenant.last_name = request.data["last_name"]
        tenant.landlord = landlord

        try:
            tenant.middle_initial = request.data["middle_initial"]
        except KeyError:
            tenant.middle_initial = None

        try:
            tenant.save()
            serializer = TenantSerializer(tenant, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single tenant
        Returns:
            Response -- JSON serialized tenant instance
        """

        try: 
            tenant = Tenant.objects.get(pk=pk)
            serializer = TenantSerializer(tenant, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        """Handle PUT requests for a tenant
        Returns:
            Response -- Empty body with 204 status code
        """
        landlord = Landlord.objects.get(user=request.auth.user)

        tenant = Tenant.objects.get(pk=pk)
        tenant.phone_number = request.data["phone_number"]
        tenant.email = request.data["email"]
        tenant.first_name = request.data["first_name"]
        tenant.middle_initial = request.data["middle_initial"]
        tenant.last_name = request.data["last_name"]
        tenant.landlord = landlord
        tenant.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single tenant
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            tenant = Tenant.objects.get(pk=pk)
            tenant.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Tenant.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to tenants resource
        Returns:
            Response -- JSON serialized list of tenants
        """
        tenants = Tenant.objects.all()
        landlord = Landlord.objects.get(user=request.auth.user)
        current_users_tenants = Tenant.objects.filter(landlord=landlord)

        serializer = TenantSerializer(
            current_users_tenants, many=True, context={'request': request}
        )
        return Response(serializer.data)


class TenantSerializer(serializers.ModelSerializer):
    """JSON serializer for tenants"""

    class Meta:
        model = Tenant
        fields = ('id', 'phone_number', 'email',
                    'first_name', 'middle_initial',
                    'last_name', 'landlord')
