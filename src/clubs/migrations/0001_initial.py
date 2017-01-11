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
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('club_name', models.CharField(max_length=200, null=True, blank=True)),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'clubs/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClubMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('club_id', models.ForeignKey(blank=True, to='clubs.Club', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='club',
            name='club_members',
            field=models.ManyToManyField(related_name='members_of_club', null=True, through='clubs.ClubMember', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='club',
            name='owner',
            field=models.ForeignKey(related_name='group_owner', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
