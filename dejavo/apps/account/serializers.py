from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from dejavo.apps.account.models import Club

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password',)
        write_only_fields = ('password',)

    def restore_object(self, attrs, instance=None):

        if instance is not None:
            instance.username = attrs.get('username', instance.username)
            instance.email = attrs.get('email', instance.email)
            instance.first_name = attrs.get('first_name', instance.first_name)
            instance.last_name = attrs.get('last_name', instance.last_name)
            if attrs.get('password') is not None:
                instance.set_password(attrs.get('password'))

            return instance

        msg = 'Instance should no be None'
        raise serializers.ValidationError(msg)


class UserSessionSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()
    
    @property
    def username_field(self):
        User = get_user_model()

        try:
            return User.USERNAME_FIELD
        except AttributeError:
            return 'username'

    def validate(self, attrs):
        credentials = {self.username_field : attrs.get(self.username_field),
                       'password' : attrs.get('password')}

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                return user
            else:
                msg = 'Unable to login with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password"'
            raise serializers.ValidationError(msg)

