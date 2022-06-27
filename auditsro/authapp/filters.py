import django_filters as filters

from .models import CustomUser


class CustomUserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='contains')

    class Meta:
        model = CustomUser
        fields = ['email', ]
