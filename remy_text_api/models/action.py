from django.db import models

class Action(models.Model):
    """Model for an accepted verb noun combo for a situation. Every situation will have certain accepted verb nouns that will have different resulting situations."""

    situation = models.ForeignKey("Situation", on_delete=models.CASCADE, related_name="resulting_action")
    verbs = models.ManyToManyField("Verb", related_name="actions")
    nouns = models.ManyToManyField("Noun", related_name="actions")
    new_situation_bool = models.BooleanField(default=False)
    new_situation = models.ForeignKey("Situation", on_delete=models.CASCADE, related_name="previous_action")
    response = models.TextField()
    get_item_bool = models.BooleanField(default=False)
    new_item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name = "find_item_action")
    required_item_bool = models.BooleanField(default=False)
    required_item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="use_item_action")
    important = models.BooleanField(default=False)