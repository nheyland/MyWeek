# Generated by Django 3.1.6 on 2021-02-25 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0003_event_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
    ]
