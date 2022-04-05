from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from basic import models, serializers, serializers_results, serializers_params, filters


# POST
# PATCH
# GET
# DELETE
# http://127.0.0.1:9000/sale/zone/
class ZoneModelViewSet(viewsets.ModelViewSet):
    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    filter_class = filters.ZoneFilter
    ordering = ('-id',)
    ordering_fields = '__all__'

    # # http://127.0.0.1:9000/sale/zone/get_by_name/
    # @action(methods=['GET'], detail=False)
    # def get_by_name(self, request, *args, **kwargs):
    #     # name = request.query_params['name']
    #     result = serializers_params.ZoneGetByNameSerializer(data=request.query_params, context={'request': request})
    #     result.is_valid(raise_exception=True)
    #     self.queryset = self.get_queryset().filter(name__icontains=result.validated_data.get('name'))
    #     return super(ZoneModelViewSet, self).list(request, *args, **kwargs)


class MaritalStatusModelViewSet(viewsets.ModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.MaritalStatusSerializer


class DepartmentModelViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class ProductGroupModelViewSet(viewsets.ModelViewSet):
    queryset = models.ProductGroup.objects.all()
    serializer_class = serializers.ProductGroupSerializer


class SupplierModelViewSet(viewsets.ModelViewSet):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer


class StateModelViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer


class EmployeeModelViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer

    @action(methods=['PATCH'], detail=True)
    def adjustment_salary(self, request, *args, **kwargs):
        percentage = request.data.get('percentage')
        employee = self.get_object()
        employee.adjustment_salary(percentage)
        employee.save()
        result = self.get_serializer(instance=employee, context=self.get_serializer_context())
        return Response(data=result.data, status=200)


class SaleModelViewSet(viewsets.ModelViewSet):
    queryset = models.Sale.objects.all()
    serializer_class = serializers.SaleSerializer

    @action(methods=['GET'], detail=False)
    def total_by_year(self, request, *args, **kwargs):
        queryset = models.Sale.objects.by_year()
        # queryset = helpers.execute_query(
        #     query=f"""
        #
        #     """
        # )
        # queryset = models.Sale.objects.raw(
        #     """
        #          SELECT EXTRACT('year' FROM s.date)::INTEGER     AS year,
        #                EXTRACT('month' FROM s.date)::INTEGER   AS month,
        #                SUM(p.sale_price * si.quantity) AS total
        #         FROM sale s
        #                  INNER JOIN sale_item si ON s.id = si.id_sale
        #                  INNER JOIN product p ON si.id_product = p.id
        #         GROUP BY EXTRACT('year' FROM s.date), EXTRACT('month' FROM s.date)
        #         ORDER BY EXTRACT('year' FROM s.date) DESC, EXTRACT('month' FROM s.date) DESC
        #     """
        # )
        # rows = [dict(zip(queryset.columns, row)) for row in [q for q in queryset.query]]
        # result = serializers_results.SaleTotalByYearSerializer(
        #     instance=queryset,
        #     many=True,
        #     context=self.get_serializer_context()
        # )
        return Response(data=queryset, status=200)
