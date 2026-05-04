from rest_framework import serializers
from ASIA_HAR_SERVER_CORE.models import User
from ASIA_HAR_SERVER_CORE.models import Patient
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)
    
    class Meta:
        model = User    
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'admin'] 


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'card_id', 'home_id']