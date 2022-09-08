from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    """Model to create a single game. One user can have several games going - this is like a save file for a single play through."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    first_name= models.CharField(max_length=25)
    current_situation = models.ForeignKey("Situation", on_delete=models.CASCADE, related_name="games")
    items = models.ManyToManyField("Item", related_name="games")