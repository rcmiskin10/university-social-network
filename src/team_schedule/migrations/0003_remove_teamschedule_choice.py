# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team_schedule', '0002_teamschedule_choice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamschedule',
            name='choice',
        ),
    ]
