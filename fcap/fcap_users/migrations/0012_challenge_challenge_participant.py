# Generated by Django 4.1 on 2022-08-09 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fcap_users', '0011_rename_player_new_rankings_participant_player_new_ratings_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_time', models.DateTimeField(null=True)),
                ('status', models.CharField(default='pending', max_length=100)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcap_users.account')),
            ],
        ),
        migrations.CreateModel(
            name='Challenge_Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcap_users.challenge')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fcap_users.account')),
            ],
        ),
    ]
