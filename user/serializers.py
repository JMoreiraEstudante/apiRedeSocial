from rest_framework import serializers
from user.models import NewUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ('id', 'email', 'user_name', 'password','photo', 'about', 'following')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('photo', 'about', 'following')


class UpdateFollowing(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('following',)