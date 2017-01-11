# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_work_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='end_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='work',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
