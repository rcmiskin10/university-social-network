# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20151219_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileinfo',
            name='major',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profileinfo',
            name='year',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[(b'Class of 2016', b'Class of 2016'), (b'Class of 2017', b'Class of 2017'), (b'Class of 2018', b'Class of 2018'), (b'Class of 2019', b'Class of 2019')]),
        ),
    ]
