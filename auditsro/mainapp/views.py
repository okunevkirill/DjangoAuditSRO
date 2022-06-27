# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .filters import OrganizationFilter, CompanyFilter
from .models import Company, Organization, Watchlist
from .serializers import CompanySerializer, OrganizationSerializer, WatchlistSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilter


class WatchlistViewSet(ModelViewSet):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
