# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_auto_20151215_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='mypost',
            name='date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='mypost',
            name='end_time',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'12AM', b'12AM'), (b'1AM', b'1AM'), (b'2AM', b'2AM'), (b'3AM', b'3AM'), (b'4AM', b'4AM'), (b'5AM', b'5AM'), (b'6AM', b'6AM'), (b'7AM', b'7AM'), (b'8AM', b'8AM'), (b'9AM', b'9AM'), (b'10AM', b'10AM'), (b'11AM', b'11AM'), (b'12PM', b'12PM'), (b'1PM', b'1PM'), (b'2PM', b'2PM'), (b'3PM', b'3PM'), (b'4PM', b'4PM'), (b'5PM', b'5PM'), (b'6PM', b'6PM'), (b'7PM', b'7PM'), (b'8PM', b'8PM'), (b'9PM', b'9PM'), (b'10PM', b'10PM'), (b'11PM', b'11PM')]),
        ),
        migrations.AddField(
            model_name='mypost',
            name='start_time',
            field=models.CharField(blank=True, max_length=10, null=True, choices=[(b'12AM', b'12AM'), (b'1AM', b'1AM'), (b'2AM', b'2AM'), (b'3AM', b'3AM'), (b'4AM', b'4AM'), (b'5AM', b'5AM'), (b'6AM', b'6AM'), (b'7AM', b'7AM'), (b'8AM', b'8AM'), (b'9AM', b'9AM'), (b'10AM', b'10AM'), (b'11AM', b'11AM'), (b'12PM', b'12PM'), (b'1PM', b'1PM'), (b'2PM', b'2PM'), (b'3PM', b'3PM'), (b'4PM', b'4PM'), (b'5PM', b'5PM'), (b'6PM', b'6PM'), (b'7PM', b'7PM'), (b'8PM', b'8PM'), (b'9PM', b'9PM'), (b'10PM', b'10PM'), (b'11PM', b'11PM')]),
        ),
    ]
