from rest_framework.relations import StringRelatedField
from rest_framework.serializers import HyperlinkedModelSerializer

from .models import Company, Organization, Watchlist


class CompanySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Company
        exclude = ('is_active',)


class OrganizationSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Organization
        exclude = ('is_active',)


class WatchlistSerializer(HyperlinkedModelSerializer):
    companies = StringRelatedField(many=True)

    class Meta:
        model = Watchlist
        fields = ('user', 'companies')
