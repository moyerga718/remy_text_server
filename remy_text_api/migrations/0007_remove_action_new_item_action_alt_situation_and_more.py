# Generated by Django 4.1.1 on 2022-09-14 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('remy_text_api', '0006_remove_action_lucidity_change'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='new_item',
        ),
        migrations.AddField(
            model_name='action',
            name='alt_situation',
            field=models.ForeignKey(default=1000, on_delete=django.db.models.deletion.CASCADE, related_name='previous_enabled_action', to='remy_text_api.situation'),
        ),
        migrations.AddField(
            model_name='action',
            name='new_items',
            field=models.ManyToManyField(related_name='actions_to_get_items', to='remy_text_api.item'),
        ),
    ]