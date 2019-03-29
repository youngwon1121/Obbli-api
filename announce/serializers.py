from rest_framework import serializers
from .models import Announce, Applying

class AnnounceSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')
    class Meta:
        model = Announce
        fields = '__all__'

class ApplyingSerializer(serializers.ModelSerializer):
    announce = serializers.ReadOnlyField(source='announce.title')
    class Meta:
        model = Applying
        fields = ('announce', 'profile', 'applier', 'id')
        read_only_fields = ('applier',)