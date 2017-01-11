# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('notifications', '0004_auto_20160106_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='club',
        ),
        migrations.AddField(
            model_name='notification',
            name='target_content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='target_object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
