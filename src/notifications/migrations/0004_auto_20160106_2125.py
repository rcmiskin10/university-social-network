# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_auto_20151205_1610'),
        ('notifications', '0003_auto_20160106_1606'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddField(
            model_name='notification',
            name='club',
            field=models.ForeignKey(blank=True, to='clubs.Club', null=True),
        ),
    ]
