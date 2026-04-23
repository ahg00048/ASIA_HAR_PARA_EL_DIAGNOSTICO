from rest_framework import serializers
from ASIA_HAR_SERVER_CORE.models import User
from ASIA_HAR_SERVER_CORE.models import Patient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__' # not password


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'