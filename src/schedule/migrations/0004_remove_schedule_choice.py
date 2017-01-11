# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_schedule_choice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='choice',
        ),
    ]
