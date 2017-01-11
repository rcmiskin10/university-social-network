# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20151217_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='company',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
