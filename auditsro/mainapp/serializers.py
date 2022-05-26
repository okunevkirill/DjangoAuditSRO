from rest_framework.serializers import ModelSerializer

from .models import Company, Organization


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
