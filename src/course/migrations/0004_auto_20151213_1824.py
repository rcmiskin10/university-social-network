# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import course.models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20151213_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syllabus',
            name='syllabus',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'protected/'), upload_to=course.models.download_loc),
        ),
    ]
