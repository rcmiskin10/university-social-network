# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_mypost_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypost',
            name='event',
            field=models.CharField(default=b'General Event', max_length=20, null=True, blank=True, choices=[(b'Party', b'Party'), (b'Game', b'Game'), (b'General Event', b'General Event')]),
        ),
    ]
