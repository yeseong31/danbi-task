from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from account.models import User


class RegisterSerializer(serializers.ModelSerializer):
    pw = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        help_text='비밀번호를 입력해 주세요.'
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'team', 'pw',)

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            team=validated_data['team'],
        )
        user.set_password(validated_data['pw'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    pw = serializers.CharField(required=True, write_only=True, validators=[validate_password],)

    class Meta:
        model = User
        fields = ('email', 'pw',)
