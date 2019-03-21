from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    selfie = serializers.ImageField(use_url=True, required=False)
    class Meta:
        model = Profile
        fields = ('owner', 'intro', 'graduated_school', 'selfie')

class UserSerializer(serializers.ModelSerializer):
    profiles = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user