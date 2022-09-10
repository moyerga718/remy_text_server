from rest_framework import serializers, status
from remy_text_api.models import Action

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'new_situation','verbs','nouns', 'required_item_bool', 'required_item' )
        depth = 1