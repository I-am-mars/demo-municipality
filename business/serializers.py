from rest_framework import serializers

from business.models import *


# Slaughterhouse serializers
class AnimalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Animal
        fields = '__all__'


class AnimalRegistrySerializer(serializers.ModelSerializer):
    animal = AnimalSerializer()

    class Meta:
        model = AnimalRegistry
        fields = ('animal', 'quantity')


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='get_full_name')

    class Meta:
        model = User
        fields = '__all__'


class RegistrySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    animals = AnimalRegistrySerializer(source='animalregistry_set', many=True)
    date = serializers.ReadOnlyField(source='get_formatted_date')

    class Meta:
        model = Registry
        fields = '__all__'


# Licenses serializers
class ActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activity
        fields = '__all__'


class LicenseSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only=True)
    status = serializers.ReadOnlyField(source='get_status')
    expired_time = serializers.ReadOnlyField(source='get_expired_time')

    class Meta:
        model = License
        fields = '__all__'