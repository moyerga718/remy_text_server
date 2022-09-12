from rest_framework import serializers, status
from remy_text_api.models import Action

class ActionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('response','new_situation_bool')