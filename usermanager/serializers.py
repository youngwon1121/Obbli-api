from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from .models import Profile, ResetPW
from announce.models import Announce, Applying
from PIL import Image
from io import BytesIO

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
    #fixed_selfie = serializers.SerializerMethodField()

    def to_representation(self, obj):
        ret = super(ProfileSerializer, self).to_representation(obj)
        return ret

    def to_internal_value(self, data):
        ret = super(ProfileSerializer, self).to_internal_value(data)
        '''
        ret['selfie'] : InMemoryUploadedFile
        ret['selfie'].name
        ret['selfie'].content_type
        ret['selfie'].file : BytesIO
        '''        

        if 'selfie' in ret:
            io = BytesIO()

            selfie = ret['selfie'].file
            im = Image.open(selfie)
            im = im.resize((200, 200))
            im.save(io, ret['selfie'].content_type.split('/')[-1].upper())

            ret['selfie'] = InMemoryUploadedFile(
                io,
                'photo',
                ret['selfie'].name,
                ret['selfie'].content_type,
                None,None
            )
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

class ResetPWSerializer(serializers.ModelSerializer):
    hash_key = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = ResetPW
        fields = ('email', 'created_at', 'hash_key')
        read_only_fields = ('verified','created_at')