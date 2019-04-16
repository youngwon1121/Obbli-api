from rest_framework import serializers
from .models import Announce, Applying, Comment

class SubCommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')
    class Meta:
        model = Comment
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')
    replies = SubCommentSerializer(many=True)
    class Meta:
        model = Comment
        read_only_fields = ('announce', 'parent')
        fields = '__all__'

class AnnounceSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')
    comments = CommentSerializer(many=True)
    instrumental_type = serializers.CharField(source='get_instrumental_type_display')

    def to_representation(self, obj):
        ret = super(AnnounceSerializer, self).to_representation(obj)
        for idx, comment in enumerate(ret['comments']):
            if comment['parent'] is not None:
                del ret['comments'][idx]

        return ret

    class Meta:
        model = Announce
        fields = '__all__'

class ApplyingSerializer(serializers.ModelSerializer):
    announce = serializers.ReadOnlyField(source='announce.title')
    class Meta:
        model = Applying
        fields = ('announce', 'profile', 'applier', 'id')
        read_only_fields = ('applier',)