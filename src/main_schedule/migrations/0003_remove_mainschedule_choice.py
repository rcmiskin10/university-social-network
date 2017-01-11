# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_schedule', '0002_mainschedule_choice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainschedule',
            name='choice',
        ),
    ]
