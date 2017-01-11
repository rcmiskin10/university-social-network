# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileinfo',
            name='loc_from',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
