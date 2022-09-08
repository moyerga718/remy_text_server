from django.db import models

class Item(models.Model):
    """Model for one item. User can pick up items throughout the course of a game - these will be added to the game inventory (join table between game and items)"""

    name = models.CharField(max_length=35)
    description = models.TextField()
    starting_item = models.BooleanField(default=False)