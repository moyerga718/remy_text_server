from django.db import models

class Noun(models.Model):
    """Model for a noun - an option that can user can input."""

    text = models.TextField()