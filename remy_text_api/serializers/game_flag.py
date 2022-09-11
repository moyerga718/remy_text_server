from rest_framework import serializers, status
from remy_text_api.models import GameFlag

class GameFlagIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameFlag
        fields = ('id',)