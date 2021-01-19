from rest_framework import serializers

from business.models import *


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