# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_members',
            field=models.ManyToManyField(related_name='members_of_team', through='teams.TeamMember', to=settings.AUTH_USER_MODEL),
        ),
    ]
