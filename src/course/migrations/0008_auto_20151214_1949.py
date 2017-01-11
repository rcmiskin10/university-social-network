# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import course.models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_auto_20151214_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syllabus',
            name='syllabus',
            field=models.FileField(upload_to=course.models.download_loc),
        ),
    ]
