from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User

from remy_text_api.models import Game
from remy_text_api.models import Action
from remy_text_api.models import Situation
from remy_text_api.models import GameFlag
from remy_text_api.models import Verb
from remy_text_api.models import Noun
from remy_text_api.models import Item
from remy_text_api.serializers import GameSerializer
from remy_text_api.serializers import ActionSerializer

class GameView(ViewSet):
    
    def retrieve(self, request, pk):
        """Get single game"""

        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def create(self, request):
        """Method for creating a game."""

        user = request.auth.user
        important_actions = Action.objects.filter(important = True)
        current_situation = Situation.objects.get(pk = 1)
        game = Game.objects.create(
            user = user,
            first_name = request.data['first_name'],
            current_situation = current_situation,
        )
        game.items.add(*request.data['items'])
        for action in important_actions:
            GameFlag.objects.create(
                game = game,
                action = action,
                completed = True
        )

        serializer = GameSerializer(game)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """method for updating a game. THIS ALL NEEDS TO CHANGE :)))"""

        """update character. This will be called whenever a choice is selected for a situation.
        Along with characterId, client will also be sending outcomeId (resulting situation) and 
        possibly itemId (if character gets a new item from the choice) as query parameters.
        """

        """
        
        #Get character
        character = Character.objects.get(pk = pk)

        #get data from query parameters
        outcomeId = request.query_params.get('outcome', None)
        itemId = request.query_params.get('item', None)

        #get situation object based on outcome id. This call will always have this query parameter, so no need for if statement
        new_situation = Situation.objects.get(pk = outcomeId)
        character.current_situation = new_situation

        #If url has itemId query parameter... 
        if itemId is not None: 
            #add that item to character
            # item = Item.objects.get(pk = itemId)
            character.items.add(itemId)

        #save the character.
        character.save()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        """

    def destroy(self, request, pk):
        """delete game"""
        game = Game.objects.get(pk = pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods = ['get'], detail = False, url_path='my_games')
    def my_games(self, request):
        user = request.auth.user
        my_games = Game.objects.filter(user = user)
        serializer = GameSerializer(my_games, many = True)
        return Response(serializer.data)

    @action(methods = ['put'], detail=True)
    def handle_action(self, request, pk):
        """This method handles the user submitting a text-based reaction for a situation. It is expecting to receive a string called "actionText" and an integer called 
        'situationId' in the request body. It is also expecting to receive the game primary key in the url. 

        This method does the following:
        1. Get current game object
        2. Get current situation object
        3. Determine whether or not the submitted text is a valid input:
            a. Split text string into several strings by space character. This will result in an array with several strings that each contain one word.
            b. Since actions can only be two words (verb + noun combo), check to make sure array length is only two. If it is not, send response saying 
            "invalid input - must be two words"
            c. See if there is a verb object and a noun object that have matching text properties that match the submitted verb/noun strings. If not, send
            back response that says "Unrecognized verb/noun".
            d. if verb and noun objects are found, continue to next step.
        4. Check to see if the submitted action is an accepted action for the current situation:
            a. Search for an action object for the current situation that has found verb + noun objects in its verbs/nouns many to many array.
            b. If an object isn't found, respond with "You can't do that here."
        5. Check to see if character must have a specific item in their inventory to complete this action.
        6. Check to see if this action is a one-time action that has already been completed: 
            a. Search for game flag object associated with found action
            b. Check to see if it has already been completed. If so, return message saying "You've already done that".
            c. If it has not been completed,
        """

        #1
        game = Game.objects.get(pk = pk)

        #2
        situation = Situation.objects.get(pk = request.data['situationId'])

        #3a
        action_text = request.data['actionText']
        action_text_array = action_text.split(" ")

        #3b
        if len(action_text_array) is not 2:
            return Response({'message': 'Invalid input. Submit verb + noun combination.'}, status=status.HTTP_204_NO_CONTENT)

        #3c
        try:
            verb = Verb.objects.get(text = action_text_array[0].lower())
        except: 
            return Response({'message': 'Unrecognized verb.'}, status=status.HTTP_204_NO_CONTENT)

        try:
            noun = Noun.objects.get(text = action_text_array[1].lower())
        except: 
            return Response({'message': 'Unrecognized noun.'}, status=status.HTTP_204_NO_CONTENT)

        #4a
        try: 
            found_action = Action.objects.get(situation = situation, verbs = verb, nouns = noun)
            # serializer = ActionSerializer(found_action)
            # return Response(serializer.data)
        #4b
        except:
            return Response({'message': "You can't do that here."}, status=status.HTTP_204_NO_CONTENT)

        #5a
        if found_action.required_item_bool is True:
            try:
                item = Item.objects.get(pk = found_action.required_item_id, pk__in = game.items.all())
                # return Response({'message': "You have the item needed for this."}, status=status.HTTP_204_NO_CONTENT)
            except: 
                return Response({'message': "You don't have the item required for this."}, status=status.HTTP_204_NO_CONTENT)

        #6a
        try:
            game_flag = GameFlag.objects.get( action = found_action)
            #6b
            if game_flag.completed is True:
                return Response({'message': "You've already done that."}, status=status.HTTP_204_NO_CONTENT)
        except: 
            pass



        
        
        return Response({'message': 'Passed test so far, keep writing that shit'}, status=status.HTTP_204_NO_CONTENT)


