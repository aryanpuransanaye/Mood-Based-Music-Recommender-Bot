from .models import Music
from rest_framework import serializers

class MusciSerializer(serializers.ModelSerializer):

    file_url = serializers.SerializerMethodField()

    class Meta:

        model = Music
        fields = ['artist', 'title', 'file_url']

    def get_file_url(self, obj):

        request = self.context.get('request')
        if request is None:
            return obj.audio_file.url  
        return request.build_absolute_uri(obj.audio_file.url)