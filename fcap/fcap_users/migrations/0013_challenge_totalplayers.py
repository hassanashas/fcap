# Generated by Django 4.1 on 2022-08-09 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcap_users', '0012_challenge_challenge_participant'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='totalPlayers',
            field=models.IntegerField(default=1),
        ),
    ]
