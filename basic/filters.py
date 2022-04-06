from django.db.models import Q, OuterRef, Exists
from django_filters import filterset
from django_filters.widgets import BooleanWidget
from basic import models


class NumberInFilter(filterset.BaseInFilter, filterset.NumberFilter):
    pass


class CharInFilter(filterset.BaseInFilter, filterset.CharFilter):
    pass


class NumberRangeFilter(filterset.BaseRangeFilter, filterset.NumberFilter):
    pass


class ZoneFilter(filterset.FilterSet):
    name = filterset.CharFilter(lookup_expr='icontains')
    active = filterset.BooleanFilter(widget=BooleanWidget)

    class Meta:
        model = models.Zone
        fields = ['name', 'active']


class EmployeeFilter(filterset.FilterSet):
    name_or_department = filterset.CharFilter(method='filter_name_or_department')
    # start_salary = filterset.NumberFilter(field_name='salary', lookup_expr='gte')
    # end_salary = filterset.NumberFilter(field_name='salary', lookup_expr='lte')
    salary_range = NumberRangeFilter(field_name='salary', lookup_expr='range')
    salary_in = NumberInFilter(field_name='salary', lookup_expr='in')
    gender_in = CharInFilter(field_name='gender', lookup_expr='in')

    @staticmethod
    def filter_name_or_department(queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(department__name__icontains=value))

    class Meta:
        model = models.Employee
        fields = ['salary_range', 'salary_in']


class ProductFilter(filterset.FilterSet):
    exists_sale = filterset.BooleanFilter(widget=BooleanWidget, method='filter_exists_sale')

    @staticmethod
    def filter_exists_sale(queryset, name, value):
        subquery = models.SaleItem.objects.filter(product=OuterRef('id'))
        return queryset.annotate(exists=Exists(subquery)).filter(exists=value)

    class Meta:
        model = models.Product
        fields = ['exists_sale']
