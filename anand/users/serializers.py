from rest_framework import serializers
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password, make_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # fields = ['email', 'first_name', 'last_name', 'usertype', 'password']
        fields = '__all__'
    
    def create(self, validated_data):
        if not validated_data['password']:
            raise serializers.ValidationError({
                'password error': _('Password cannot be empty')
            })
        elif len(validated_data['password']) < 8:
            raise serializers.ValidationError({
                'password error': _('Password is to short, should be greater that 8 characters')
            })
        try:
            user = CustomUser.objects.get(email=validated_data['email'])
        except CustomUser.DoesNotExist:
            user = None
        if user:
            raise serializers.ValidationError({
                'email error': _('Email already exist')
            })

        validated_data['password'] = make_password(validated_data['password'])
        return CustomUser.objects.create(**validated_data)
    
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']
