# Generated by Django 4.1 on 2022-08-09 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcap_users', '0014_challenge_participant_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='type',
            field=models.CharField(default='member', max_length=255),
        ),
    ]