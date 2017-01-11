# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frat_schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fratschedule',
            name='choice',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
