from rest_framework import serializers
from .models import Announce, Applying, Comment

class AnnounceSerializer(serializers.ModelSerializer):
    writer_name = serializers.CharField(source='writer.username', read_only=True)
    instrument_name = serializers.CharField(source='instrument.name', read_only=True)

    class Meta:
        model = Announce
        fields = '__all__'

class SubCommentSerializer(serializers.ModelSerializer):
    writer_name = serializers.CharField(source='writer.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    wrtier_name = serializers.CharField(source='writer.username', read_only=True)
    replies = SubCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

class AnnounceSerializer2(serializers.ModelSerializer):
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