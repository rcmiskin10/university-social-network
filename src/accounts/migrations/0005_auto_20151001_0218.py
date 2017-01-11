# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20151001_0206'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='user_permissions',
        ),
    ]
