from rest_framework import serializers


class ZoneGetByNameSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=64)
