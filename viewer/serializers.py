from rest_framework import serializers

from viewer.models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'description', 'chord_image', 'chord_url']