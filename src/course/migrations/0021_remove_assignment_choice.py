# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0020_assignment_choice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='choice',
        ),
    ]
