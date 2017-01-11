# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0003_auto_20151022_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='event',
            field=models.CharField(default=b'General Event', max_length=20, choices=[(b'Party', b'Party'), (b'Game', b'Game'), (b'General Event', b'General Event')]),
        ),
    ]
