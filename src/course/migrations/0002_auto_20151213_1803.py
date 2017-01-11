# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syllabus',
            name='syllabus',
            field=models.FileField(upload_to=b'/protected'),
        ),
    ]
