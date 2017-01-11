# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frat_schedule', '0002_fratschedule_choice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fratschedule',
            name='choice',
        ),
    ]
