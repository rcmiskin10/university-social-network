# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_bio_dreamjob_interest_work'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bio',
            old_name='text',
            new_name='bio',
        ),
    ]
