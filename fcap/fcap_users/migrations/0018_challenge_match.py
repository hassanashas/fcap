# Generated by Django 4.1 on 2022-08-16 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fcap_users', '0017_challenge_challenge_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='match',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='fcap_users.match'),
        ),
    ]