# Generated by Django 4.1 on 2022-08-07 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcap_users', '0009_alter_match_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='player_new_rankings',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='participant',
            name='player_prev_rankings',
            field=models.FloatField(null=True),
        ),
    ]
