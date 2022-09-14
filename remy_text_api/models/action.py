from django.db import models

class Action(models.Model):
    """Model for an accepted verb noun combo for a situation. Every situation will have certain accepted verb nouns that will have different resulting situations."""

    situation = models.ForeignKey("Situation", on_delete=models.CASCADE, related_name="resulting_action")
    verbs = models.ManyToManyField("Verb", related_name="actions")
    nouns = models.ManyToManyField("Noun", related_name="actions")
    new_situation_bool = models.BooleanField(default=False)
    new_situation = models.ForeignKey("Situation", on_delete=models.CASCADE, related_name="previous_action")
    alt_situation = models.ForeignKey("Situation", on_delete=models.CASCADE, related_name="previous_enabled_action", default= 1000)
    display_response_on_complete = models.BooleanField(default=True)
    response = models.TextField()
    get_item_bool = models.BooleanField(default=False)
    new_items = models.ManyToManyField("Item", related_name="actions_to_get_items")
    required_item_bool = models.BooleanField(default=False)
    required_item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="required_item_action")
    important = models.BooleanField(default=False)
    use_item_bool = models.BooleanField(default=False)
    use_item = models.ForeignKey("Item", default=999, on_delete=models.CASCADE, related_name="use_item_action")
    #ids of other actions that, if completed, ALLOW you to do this. For example, unlocking a door allows you to open the door. 
    enable_action_dependencies = models.ManyToManyField("Action", related_name="enabled_actions")
    #ids of other actions that, if completed, would cause you to not be able to do this. 
    disable_action_dependencies = models.ManyToManyField("Action", related_name="disabled_actions")
