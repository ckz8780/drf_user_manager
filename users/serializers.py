from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

import django.contrib.auth.password_validation as django_pw_validators

class UserSerializer(serializers.ModelSerializer):

    # Validate that emails are unique as well as usernames
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',) # Just so we know for deletions/updates

    def validate(self, data):
        print("validating...")
        """
        Validate passwords by utilizing Django's built in validators
        """
        user = User(**data)
        errors = dict()
        try:
            django_pw_validators.validate_password(password=data.get('password'), user=user)
        except ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)

    def create(self, validated_data):
        """
        We need to override the default create method or the ModelSerializer
        will not hash passwords correctly. 
        """
        user = User.objects.create_user(**validated_data)
        return user