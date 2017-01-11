# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('local', '0003_place_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='distance',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
