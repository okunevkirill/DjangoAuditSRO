# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Company, Organization, Watchlist
from .serializers import CompanySerializer, OrganizationSerializer, WatchlistSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class WatchlistViewSet(ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
