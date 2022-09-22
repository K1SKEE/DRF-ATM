from rest_framework import serializers

from .models import *


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('user_permissions', 'groups', 'is_active',
                   'is_superuser', 'password',)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number')

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number')
        )
        return user


class UserIsOwnerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('iban', 'username', 'last_name', 'first_name', 'phone_number')

# user = serializers.HiddenField(default=serializers.CurrentUserDefault)
