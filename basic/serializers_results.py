from rest_framework import serializers


class SaleTotalByYearSerializer(serializers.Serializer):
    year = serializers.IntegerField(read_only=True, source='date__year')
    month = serializers.IntegerField(read_only=True, source='date__month')
    total = serializers.DecimalField(read_only=True, max_digits=16, decimal_places=2)
