from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Profile, ResetPW
from announce.models import Announce, Applying
from PIL import Image
from io import BytesIO

User = get_user_model()

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        '''
            fields : 사용하고자하는 필드
        '''
        fields = kwargs.pop('fields', None)
        
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)
        
        if fields is not None:
            fields = set(self.fields) - set(fields)

            for field_name in fields:
                self.fields.pop(field_name)

class UserSerializer(DynamicFieldsModelSerializer):
    profiles = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='my-profile-detail',
        read_only=True
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'userid', 'username', 'phone', 'date_of_birth', 'email', 'graduated_school', 'profiles', 'password')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    selfie = serializers.ImageField(use_url=True, required=False)
    #fixed_selfie = serializers.SerializerMethodField()

    def to_internal_value(self, data):
        '''
        ret['selfie'] : InMemoryUploadedFile
        ret['selfie'].name
        ret['selfie'].content_type
        ret['selfie'].file : BytesIO
        '''        
        ret = super(ProfileSerializer, self).to_internal_value(data)
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
                None, None
            )
        return ret

    class Meta:
        model = Profile
        read_only_fields = ('owner', )
        fields = ('owner', 'intro', 'selfie', 'id', )

class MyAnnounceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announce
        fields = '__all__'

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'date_of_birth', 'email', 'graduated_school',)

class ApplyingSerializer(serializers.ModelSerializer):
    applier = SimpleUserSerializer()
    selfie = serializers.ImageField(source='profile.selfie', use_url=True, read_only=True)
    intro = serializers.ReadOnlyField(source='profile.intro')

    class Meta:
        model = Applying
        fields = ('applier', 'selfie', 'intro',)

class AnnounceDetailSerializer(serializers.ModelSerializer):
    applying = ApplyingSerializer(many=True)
    class Meta:
        model = Announce
        fields = '__all__'

class MyAppliedSerializer(serializers.ModelSerializer):
    announce = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='announce:announce-detail'
    )
    announce_title = serializers.ReadOnlyField(source='announce.title')
    announce_deadline = serializers.ReadOnlyField(source='announce.deadline')
    class Meta:
        model = Applying
        fields = ('id', 'announce', 'announce_title', 'announce_deadline', 'created_at', 'profile')

class ResetPWSerializer(serializers.ModelSerializer):
    hash_key = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = ResetPW
        fields = ('email', 'created_at', 'hash_key')
        read_only_fields = ('verified', 'created_at')

class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = '__all__'