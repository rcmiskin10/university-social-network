# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.files.storage
import course.models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_auto_20151214_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='html',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='syllabus',
            name='syllabus',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/rcmiskin/Desktop/student_g/src/media/protected'), upload_to=course.models.download_loc),
        ),
    ]
