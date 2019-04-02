from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile
from announce.models import Announce, Applying

User = get_user_model()

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

class ProfileSerializer(serializers.ModelSerializer):
    my_apply = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    selfie = serializers.ImageField(use_url=True, required=False)
    def to_representation(self, obj):
        ret = super(ProfileSerializer, self).to_representation(obj)
        return ret

    class Meta:
        model = Profile
        read_only_fields = ('owner', 'my_apply')
        fields = ('owner', 'intro', 'selfie', 'id', 'my_apply')

class MyAnnounceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announce
        fields = '__all__'

class ApplyingSerializer(serializers.ModelSerializer):
    applier = UserSerializer()
    selfie = serializers.ImageField(source='profile.selfie', use_url=True, read_only=True)
    intro = serializers.ReadOnlyField(source='profile.intro')

    def to_representation(self, instance):
        worthless_list = ['profiles', 'last_login', 'is_superuser', 'is_active', 'is_admin', 'groups', 'user_permissions']
        ret = super(ApplyingSerializer, self).to_representation(instance)

        for worthless in worthless_list:
            del ret['applier'][worthless]
        return ret

    class Meta:
        model = Applying
        fields = ('applier', 'selfie', 'intro',)

class AnnounceDetailSerializer(serializers.ModelSerializer):
    applying = ApplyingSerializer(many=True)
    class Meta:
        model = Announce
        fields = '__all__'

class MyAppliedSerializer(serializers.ModelSerializer):
    announce_title = serializers.ReadOnlyField(source='announce.title')
    announce_deadline = serializers.ReadOnlyField(source='announce.deadline')
    class Meta:
        model = Applying
        fields = '__all__'