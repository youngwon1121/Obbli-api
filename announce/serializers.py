from rest_framework import serializers
from .models import Announce, Applying, Comment

class SubCommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')
    class Meta:
        model = Comment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')
    replies = SubCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        read_only_fields = ('announce',)
        fields = '__all__'

class AnnounceSerializerForList(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')
    instrumental_type = serializers.CharField(source='get_instrumental_type_display')
    url = serializers.HyperlinkedIdentityField(
        view_name = 'announce:announce-detail'
    )

    class Meta:
        model = Announce
        fields = ('id', 'url', 'title', 'writer', 'instrumental_type', 'deadline', 'pay')

class AnnounceSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')
    comments = CommentSerializer(many=True)
    instrumental_type = serializers.CharField(source='get_instrumental_type_display')

    def to_representation(self, obj):
        ret = super(AnnounceSerializer, self).to_representation(obj)
        ret['comments'] = [comment for comment in ret['comments'] if comment['parent'] is None]
        return ret
        
    class Meta:
        model = Announce
        fields = ('id', 'writer', 'instrumental_type', 'title', 'content', 'pay', 'locations', 'deadline', 'comments')

class ApplyingSerializer(serializers.ModelSerializer):
    announce = serializers.ReadOnlyField(source='announce.title')
    class Meta:
        model = Applying
        fields = ('announce', 'profile', 'applier', 'id')
        read_only_fields = ('applier',)