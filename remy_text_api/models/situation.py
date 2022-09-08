from django.db import models

class Situation(models.Model):
    """Model for a situation - this is a prompt that will be given to the user that will have several choices affiliated with it."""

    text = models.TextField()
    location = models.CharField(max_length=30)