# Generated by Django 3.1.7 on 2021-02-28 17:00

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userprofile',
            managers=[
                ('objects', accounts.models.ProfileManager()),
            ],
        ),
    ]
