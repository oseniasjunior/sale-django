from kombu import BrokerConnection
from kombu.exceptions import OperationalError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from basic import models, serializers, tasks, filters


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

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.prefetch_related('product_set')
        return super(SupplierModelViewSet, self).list(request, *args, **kwargs)


class StateModelViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer


class EmployeeModelViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    filter_class = filters.EmployeeFilter

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
        try:
            tasks.sale_by_year.apply_async([])
        except OperationalError as error:
            raise Exception(f'Broker connection error {error}')
        return Response(status=200)


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_class = filters.ProductFilter

    def list(self, request, *args, **kwargs):
        expand = request.query_params.get('expand', None)
        if expand is not None:
            relations = expand.split(',')
            for r in relations:
                self.queryset = self.queryset.select_related(r)
        return super(ProductModelViewSet, self).list(request, *args, **kwargs)

    # def retrieve(self, request, *args, **kwargs):
    #     self.queryset = self.queryset.select_related('supplier')
    #     return super(ProductModelViewSet, self).retrieve(request, *args, **kwargs)

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
