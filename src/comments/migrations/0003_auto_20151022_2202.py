# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20151022_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypost',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
