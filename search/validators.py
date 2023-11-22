from rest_framework import serializers


def validate_query_length(value):
    if len(value) < 3:
        raise serializers.ValidationError("Query must be at least 3 characters long.")
