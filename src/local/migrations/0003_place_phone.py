# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('local', '0002_auto_20151207_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='phone',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]
