from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q

from remy_text_api.models import GameFlag

class GameFlagView(ViewSet):
    """Viewset to handle changes in game flags."""

    @action(methods=['put'], detail=True)
    def completed(self,request,pk):
        """This action locates a GameFlag object based on actionId and gameId and flips completed to TRUE
        """
        characterId = request.query_params.get('character', None)
        try:
            game_flag = GameFlag.objects.get(action_id=pk, character_id=characterId)
            game_flag.completed = True
            game_flag.save()
        except:
            pass
        return Response(None, status=status.HTTP_204_NO_CONTENT)