from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profiles = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    applied = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'
    
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    owner = UserSerializer()
    selfie = serializers.ImageField(use_url=True, required=False)
    my_apply = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    def to_representation(self, obj):
        ret = super(ProfileSerializer, self).to_representation(obj)
        return ret

    class Meta:
        model = Profile
        read_only_fields = ('owner', 'my_apply')
        fields = ('owner', 'intro', 'selfie', 'id', 'my_apply')