# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Company, Organization
from .serializers import CompanySerializer, OrganizationSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
