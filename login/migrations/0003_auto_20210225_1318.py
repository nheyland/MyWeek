# Generated by Django 3.1.7 on 2021-02-25 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friends',
            name='friend',
            field=models.ManyToManyField(related_name='friends', to='login.User'),
        ),
    ]
