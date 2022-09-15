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
from remy_text_api.serializers import GameFlagIdSerializer
from remy_text_api.serializers import ActionResponseSerializer


class GameView(ViewSet):

    def retrieve(self, request, pk):
        """Get single game"""

        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def create(self, request):
        """Method for creating a game."""

        user = request.auth.user
        important_actions = Action.objects.filter(important=True)
        current_situation = Situation.objects.get(pk=1)
        game = Game.objects.create(
            user=user,
            first_name=request.data['first_name'],
            current_situation=current_situation,
        )
        game.items.add(*request.data['items'])
        game.starting_item = Item.objects.get(pk=request.data['items'][0])
        for action in important_actions:
            GameFlag.objects.create(
                game=game,
                action=action,
                completed=False
            )

        serializer = GameSerializer(game)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """delete game"""
        game = Game.objects.get(pk=pk)
        game.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path='my_games')
    def my_games(self, request):
        user = request.auth.user
        my_games = Game.objects.filter(user=user)
        serializer = GameSerializer(my_games, many=True)
        return Response(serializer.data)

    @action(methods=['put'], detail=True)
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
        5. Check to see if character must have a specific item in their inventory to complete this action:
            a. If required_item_bool is true, see if that item is in the game's inventory
            b. If user does not have this item in this game yet, return a response saying "You don't have the item required"
        6. Check to see if this action relies on another action to be completed first
        7. Check to see if this action is a one-time action that has already been completed OR cannot be completed because another action that disables it has already been completed: 
            a. Search for game flag object associated with found action
            b. Check to see if it has already been completed. If so, return message saying "You've already done that".
            c. If it has not been completed, mark game flag object as completed and continue. 
        8. If player receives an item by completing this action, add that item to their inventory:
            a. See if get_item_bool on action is true or false.
            b. if true, find item object and add that item to game.items.
        9. If player consumes an item by completing this action, remove that item from their inventory.
        10. Check to see if the character goes to a new situation after performing this action
            a. See if new_situation_bool is true or false.
            b. if true, get new situation object using new_situation_id on action and update it on game object
        11. Time to package up all necessary data and send it back to client in response. We need:
            a. Game data (now possibly updated with new situation object and new item object.)
            b. id of game flag that was marked true (if flag was marked true)
            c. Response from action object.
            d. boolean saying that action was completed. 
        """

        # 1
        game = Game.objects.get(pk=pk)

        # 2
        situation = Situation.objects.get(pk=request.data['situationId'])

        # 3a
        action_text = request.data['actionText']
        action_text_array = action_text.split(" ")

        # Dictionary that will be sent as a response whenever action can't be completed. Message object will be updated with appropriate text prior to sending response.
        response_data = {
            "action_completed": False,
            "message": ""
        }

        # 3b
        if len(action_text_array) != 2:
            response_data["message"] = "Invalid input. Submit verb + noun combination."
            return Response(response_data)

        # 3c
        try:
            verb = Verb.objects.get(text=action_text_array[0].lower())
        except:
            response_data["message"] = "Unrecognized verb."
            return Response(response_data)

        try:
            noun = Noun.objects.get(text=action_text_array[1].lower())
        except:
            response_data["message"] = "Unrecognized noun."
            return Response(response_data)

        # 4a
        try:
            found_action = Action.objects.get(
                situation=situation, verbs=verb, nouns=noun)
        # 4b
        except:
            response_data["message"] = "You can't do that here."
            return Response(response_data)

        # CHECK TO SEE IF USER IS TRIGGERING THE END OF THE GAME.

        if found_action.id == 113:
            #See if user has given the man all four teeth in this game:
            try:
                tooth1_flag = GameFlag.objects.get(action_id = 31, game=game, completed=True)
                tooth2_flag = GameFlag.objects.get(action_id = 32, game=game, completed=True)
                tooth3_flag = GameFlag.objects.get(action_id = 33, game=game, completed=True)
                tooth4_flag = GameFlag.objects.get(action_id = 34, game=game, completed=True)
            except: 
                pass
            
            #See if user has given the man all four gems in this game:
            try:
                gem1_flag = GameFlag.objects.get(action_id = 27, game=game, completed=True)
                gem2_flag = GameFlag.objects.get(action_id = 28, game=game, completed=True)
                gem3_flag = GameFlag.objects.get(action_id = 29, game=game, completed=True)
                gem4_flag = GameFlag.objects.get(action_id = 30, game=game, completed=True)
            except: 
                pass

            #If they haven't completed this, reset all game flags and clear inventory for this game.
            all_flags = GameFlag.objects.filter(game=game)
            for flag in all_flags:
                flag.completed = False
                flag.save()
            

        # 5
        if found_action.required_item_bool is True:
            # 5a
            try:
                req_item = Item.objects.get(
                    pk=found_action.required_item_id, pk__in=game.items.all())
            # 5b
            except:
                response_data["message"] = "You don't have the item required for this."
                return Response(response_data)

        #6
        try:
            necessary_completed_actions = Action.objects.filter(pk__in = found_action.enable_action_dependencies.all())
            for necessary_action in necessary_completed_actions:
                found_game_flag = GameFlag.objects.get(game=game, action=necessary_action)
                if found_game_flag.completed is False:
                    response_data["message"] = found_action.response
                    return Response(response_data)
        except:
            pass

        # 7a
        completed_game_flag_ids = []
        try:
            game_flag = GameFlag.objects.get(action=found_action, game=game)
            # 7b
            if game_flag.completed is True:
                response_data["message"] = "You've already done that."
                return Response(response_data)
            # 7c
            else:
                game_flag.completed = True
                game_flag.save()
                completed_game_flag_ids.append(game_flag.id)
                try:
                    dependent_actions = Action.objects.filter(pk__in= found_action.disable_action_dependencies.all())
                    for dependent_action in dependent_actions:
                        found_game_flag = GameFlag.objects.get(game=game, action = dependent_action)
                        found_game_flag.completed = True
                        found_game_flag.save()
                        completed_game_flag_ids.append(found_game_flag.id)
                except: 
                    pass
        except:
            pass

        # 8a
        if found_action.get_item_bool is True:
            # 8b
            for new_item in found_action.new_items.all():
                new_item = Item.objects.get(pk=new_item.id)
                game.items.add(new_item)
                game.save()

        # 9a 
        if found_action.use_item_bool is True: 
            used_item = Item.objects.get(pk=found_action.use_item_id)
            game.items.remove(used_item)
            game.save()

        # 10a
        if found_action.new_situation_bool is True:
            # 9b
            new_situation = Situation.objects.get(
                pk=found_action.new_situation_id)
            game.current_situation = new_situation
            game.save()

        # 11
        game_serializer = GameSerializer(game)
        # game_flag_serializer = GameFlagIdSerializer(game_flag)
        found_action_serializer = ActionResponseSerializer(found_action)

        response_data = {
            "action_completed": True,
            "game_data": game_serializer.data,
            "completed_game_flag_ids": completed_game_flag_ids,
            "action_response": found_action_serializer.data
        }

        return Response(response_data)
