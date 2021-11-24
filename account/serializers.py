from django.contrib.auth import password_validation
from rest_framework import serializers
from .models import CustomUser
from django.utils.translation import gettext, gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm


class RegistrationSerializers(RegistrationForm):

    class Meta:
        model = CustomUser
        fields = ['id',"email","Full_Name","Gender",'Marital_Status',"Mother_Tongue","Mobile_No","password1","password2"]


class CustomUserSerializers(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     if validated_data.get('password'):
    #         validated_data['password'] = make_password(validated_data['password'])
    #     return super().create(validated_data)

    class Meta:
        model = CustomUser
        fields = ['id',"email","Full_Name","Gender",'Marital_Status',"Mother_Tongue","Mobile_No"]


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
