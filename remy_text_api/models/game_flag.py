from django.db import models

class GameFlag(models.Model):
    """Model to keep track of game flags. These objects are flags to mark when notable events in the game have happened for a character, such as picking up an item, 
    to make sure you can't do the same major event twice."""

    game = models.ForeignKey("Game", on_delete=models.CASCADE, related_name="game_flags")
    action = models.ForeignKey("Action", on_delete=models.CASCADE, related_name="game_flags", default= 1)
    completed = models.BooleanField(default=False) 