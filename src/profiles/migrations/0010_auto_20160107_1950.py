# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20151221_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpicture',
            name='image',
            field=models.ImageField(default=b'/home/rcmiskin/Desktop/student_g/src/static/static/img/default-prof.png', upload_to=b'profiles/'),
        ),
    ]
