from rest_framework import serializers
from packages.models import Package
from django.contrib.auth.models import User

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['id', 'name', 'version', 'url', 'content']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_staff']

    def create(self, validated_data):
        # method borrowed from https://stackoverflow.com/questions/27586095/why-isnt-my-django-user-models-password-hashed
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class RatingSerializer(serializers.Serializer):
    BusFactor = serializers.DecimalField(max_digits=3, decimal_places=1)
    Correctness = serializers.DecimalField(max_digits=3, decimal_places=1)
    RampUp = serializers.DecimalField(max_digits=3, decimal_places=1)
    ResponsiveMaintainer = serializers.DecimalField(max_digits=3, decimal_places=1)
    LicenseScore = serializers.DecimalField(max_digits=3, decimal_places=1)
    GoodPinningPractice = serializers.DecimalField(max_digits=3, decimal_places=1)