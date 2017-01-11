# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frats', '0002_auto_20151205_1610'),
        ('comments', '0012_mypost_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='frat',
            field=models.ForeignKey(blank=True, to='frats.Frat', null=True),
        ),
    ]
