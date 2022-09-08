from django.db import models

class SituationVerbNoun(models.Model):
    """Model for an accepted verb noun combo for a situation. Every situation will have certain accepted verb nouns that will have different resulting situations."""

    situation = models.ForeignKey("Situation", on_delete=models.CASCADE, related_name="resulting_svns")
    noun = models.ForeignKey("Noun", on_delete=models.CASCADE, related_name="svns")
    verb = models.ForeignKey("Verb", on_delete=models.CASCADE, related_name="svns")
    outcome_situation = models.ForeignKey("Situation", on_delete=models.CASCADE, related_name="previous_svns")
    response = models.TextField()
    get_item_bool = models.BooleanField(default=False)
    new_item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name = "find_item_svns")
    required_item_bool = models.BooleanField(default=False)
    required_item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="use_item_svns")
    important = models.BooleanField(default=False)