# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_coursenote'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='choice',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
