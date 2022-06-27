import django_filters as filters

from .models import Organization, Company


class OrganizationFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')
    tax_number = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Organization
        fields = ['name', 'tax_number']


class CompanyFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')
    tax_number = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = Company
        fields = ['name', 'tax_number']
