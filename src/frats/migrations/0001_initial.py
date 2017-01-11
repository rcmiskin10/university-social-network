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
            name='Frat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True, blank=True)),
                ('frat_or_sorority', models.CharField(max_length=15, choices=[(b'Fraternity', b'Fraternity'), (b'Sorority', b'Sorority')])),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'frats/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frat_id', models.ForeignKey(blank=True, to='frats.Frat', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='frat',
            name='members',
            field=models.ManyToManyField(related_name='members_of_frat', null=True, through='frats.Member', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='frat',
            name='owner',
            field=models.ForeignKey(related_name='frat_owner', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
