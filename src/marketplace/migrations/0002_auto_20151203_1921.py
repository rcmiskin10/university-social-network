# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(max_length=15, choices=[(b'Textbook', b'Textbook'), (b'Electronics', b'Electronics'), (b'Room', b'Room'), (b'Tutors', b'Tutors'), (b'Housing', b'Housing'), (b'Other', b'Other')]),
        ),
    ]
