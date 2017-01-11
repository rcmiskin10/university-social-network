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
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=15, choices=[(b'Textbook', b'Textbook'), (b'Electronis', b'Electronics'), (b'Room', b'Room'), (b'Tutors', b'Tutors'), (b'Housing', b'Housing'), (b'Other', b'Other')])),
                ('price', models.CharField(max_length=100)),
                ('order', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to=b'products/')),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-order'],
            },
        ),
    ]
