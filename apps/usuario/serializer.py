from .models import FirmaDigital
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
import base64
from django.core.files.base import ContentFile
import re

class SerializerUsuario(serializers.ModelSerializer):
    """
    Serializer for User model with group information.
    """
    name_group = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def get_name_group(self, obj):
        groups =  obj.groups.all()
        groups_name =  [ i.name for i in groups]
        if len(groups_name) > 0 : 
            return groups_name[0]
        else:
            return ""

    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        password = validated_data.pop('password')
        
        user = User.objects.create_user(
            password=password,
            **validated_data
        )
        
        if groups:
            user.groups.set(groups)
        return user

class SerializerUpdateUsuario(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'groups']

class SerializerReadUsuario(serializers.ModelSerializer):
    name_group = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'groups', 'name_group']

    def get_name_group(self, obj):
        groups =  obj.groups.all()
        groups_name =  [ i.name for i in groups]
        if len(groups_name) > 0 : 
            return groups_name[0]
        else:
            return ""


class changePasswordSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['password']
        
class SerializerEmpleado(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']


class SerializerGroups(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token =  super().get_token(user)
        serializer_data =  SerializerReadUsuario(user)
        token["usuario"] = serializer_data.data
        return token

class FirmaDigitalSerializer(serializers.ModelSerializer):  
    class Meta:
        model = FirmaDigital
        fields = '__all__'
    