# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_auto_20151213_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syllabus',
            name='syllabus',
            field=models.FileField(upload_to=b'protected/'),
        ),
    ]
