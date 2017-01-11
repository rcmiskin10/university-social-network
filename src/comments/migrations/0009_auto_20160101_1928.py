# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_mypost_main'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypost',
            name='path',
            field=models.CharField(max_length=350, null=True, blank=True),
        ),
    ]
