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
import json

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
        tenant.full_name = request.data["full_name"]
        tenant.landlord = landlord


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
        tenant.full_name = request.data["full_name"]
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
        landlord = Landlord.objects.get(user=request.auth.user)
        current_users_tenants = Tenant.objects.filter(landlord=landlord)

        table = self.request.query_params.get('table', None)

        if table is not None:
            tenant_obj = {}
            for tenant in current_users_tenants:
                tenant_obj[tenant.id] = tenant.full_name
            
            to_string = json.dumps(tenant_obj, separators=None)

            return Response(to_string)
        
        serializer = TenantSerializer(
            current_users_tenants, many=True, context={'request': request}
        )
        return Response(serializer.data)


class TenantSerializer(serializers.ModelSerializer):
    """JSON serializer for tenants"""

    class Meta:
        model = Tenant
        fields = ('id', 'phone_number', 'email',
                    'landlord', 'full_name')
