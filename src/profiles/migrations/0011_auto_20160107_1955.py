# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20160107_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpicture',
            name='image',
            field=models.ImageField(upload_to=b'profiles/'),
        ),
    ]
