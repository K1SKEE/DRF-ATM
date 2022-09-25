from rest_framework import serializers

from .models import *


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('user_permissions', 'groups', 'is_active',
                   'is_superuser', 'password',)


class UserDetailSerializer(serializers.ModelSerializer):
    wallet = serializers.SlugRelatedField(
        slug_field='card_number', read_only=True, many=True
    )

    class Meta:
        model = User
        exclude = ('password',)


class UserRegisterSerializer(serializers.ModelSerializer):
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


class UserChangePinSerializer(serializers.ModelSerializer):
    pin1 = serializers.CharField(max_length=4, min_length=4)
    pin2 = serializers.CharField(max_length=4, min_length=4)

    class Meta:
        model = User
        fields = ('password', 'pin1', 'pin2')

    def update(self, instance, validated_data):
        result = instance.change_pin(
            validated_data['password'],
            validated_data['pin1'],
            validated_data['pin2']
        )
        instance.save()
        return result


class UserIsOwnerDetailSerializer(serializers.ModelSerializer):
    wallet = serializers.SlugRelatedField(
        slug_field='card_number', read_only=True, many=True
    )

    class Meta:
        model = User
        fields = ('iban', 'username', 'last_name', 'first_name', 'phone_number',
                  'wallet')


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class CardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Card
        fields = ('currency', 'user')

    def create(self, validated_data):
        card = Card.objects.create(validated_data)
        return f'Нова карта {card.card_number} {card.currency} створена'
