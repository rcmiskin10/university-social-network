# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20151205_1610'),
        ('comments', '0011_mypost_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='team',
            field=models.ForeignKey(blank=True, to='teams.Team', null=True),
        ),
    ]
