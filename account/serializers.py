from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User, Team


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],  # 이메일 중복 검증
    )
    pw = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],  # 비밀번호 검증
    )
    pw2 = serializers.CharField(
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'team', 'pw', 'pw2',)

    def validate(self, data):
        """비밀번호 일치 여부 확인"""
        if data['pw'] != data['pw2']:
            raise serializers.ValidationError({'pw': "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['pw'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'team',)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name',)
