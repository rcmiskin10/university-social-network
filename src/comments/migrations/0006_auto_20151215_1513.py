# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_auto_20151215_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypost',
            name='event',
            field=models.CharField(default=None, max_length=20, null=True, blank=True, choices=[(b'Party', b'Party'), (b'Game', b'Game'), (b'General Event', b'General Event')]),
        ),
    ]
