# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('local', '0004_place_distance'),
        ('comments', '0014_mypost_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='place',
            field=models.ForeignKey(blank=True, to='local.Place', null=True),
        ),
    ]
