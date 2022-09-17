from rest_framework import serializers, status
from remy_text_api.models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id','first_name','current_situation','items', 'completed')
        depth = 1