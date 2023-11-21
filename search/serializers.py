from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255, required=True)
