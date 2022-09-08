from django.db import models

class Verb(models.Model):
    """Model for a verb - an option that can user can input."""

    text = models.TextField()