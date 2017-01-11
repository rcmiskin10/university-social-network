# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_auto_20151205_1610'),
        ('comments', '0010_mypost_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='club',
            field=models.ForeignKey(blank=True, to='clubs.Club', null=True),
        ),
    ]
