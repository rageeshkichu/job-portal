from rest_framework import serializers
from .models import Employer

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ['name', 'email', 'mobile', 'password', 'logo', 'website', 'address']
