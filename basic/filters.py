from django_filters import filterset
from django_filters.widgets import BooleanWidget
from basic import models


class ZoneFilter(filterset.FilterSet):
    name = filterset.CharFilter(lookup_expr='icontains')
    active = filterset.BooleanFilter(widget=BooleanWidget)

    class Meta:
        model = models.Zone
        fields = ['name', 'active']
