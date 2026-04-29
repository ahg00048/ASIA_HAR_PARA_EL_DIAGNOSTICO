from rest_framework import serializers
from ASIA_HAR_SERVER_CORE.models import User
from ASIA_HAR_SERVER_CORE.models import Patient


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User    
        fields = ['name', 'first_name', 'last_name', 'email'] 


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'idCard', 'homeId']