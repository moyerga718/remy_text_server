# Generated by Django 4.1.1 on 2022-09-13 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('remy_text_api', '0005_action_disable_action_dependencies_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='lucidity_change',
        ),
    ]
