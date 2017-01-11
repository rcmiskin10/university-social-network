# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.CharField(max_length=20, choices=[(b'Class of 2016', b'Class of 2016'), (b'Class of 2017', b'Class of 2017'), (b'Class of 2018', b'Class of 2018'), (b'Class of 2019', b'Class of 2019')])),
                ('major', models.CharField(max_length=100)),
                ('minor', models.CharField(max_length=100, null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
