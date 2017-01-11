# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=b'local/', blank=True)),
                ('name', models.CharField(max_length=100)),
                ('rating', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=200)),
                ('website', models.URLField(max_length=300, null=True, blank=True)),
                ('delivery', models.BooleanField(default=False)),
                ('hours', models.CharField(max_length=100, null=True, blank=True)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('menu', models.URLField(max_length=300, null=True, blank=True)),
                ('category', models.ManyToManyField(related_name='cat', to='local.Category')),
            ],
        ),
    ]
