# Generated by Django 4.1 on 2022-08-09 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcap_users', '0015_account_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='expiry_time',
            field=models.DateTimeField(null=True),
        ),
    ]
