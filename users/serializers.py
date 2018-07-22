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
        read_only_fields = ('id',)

    def validate(self, data):
        """
        Validate passwords by utilizing Django's built in validators
        """
        user = User(**data)
        password = data.get('password')
        errors = dict()
        
        try:
            django_pw_validators.validate_password(password=password, user=user)
        except ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSerializer, self).validate(data)