from rest_framework import serializers
from packages.models import Package

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['id', 'name', 'version', 'url']