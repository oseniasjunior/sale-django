from rest_framework import serializers


class EmployeeSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    district = serializers.CharField(read_only=True, source='district__name')
    city = serializers.CharField(read_only=True, source='district__city__name')
    state = serializers.CharField(read_only=True, source='district__city__state__name')
