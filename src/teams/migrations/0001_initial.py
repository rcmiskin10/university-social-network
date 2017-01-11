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
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, blank=True)),
                ('choice', models.CharField(max_length=30, choices=[(b'Intramural', b'Intramural'), (b'Club', b'Club'), (b'Varsity', b'Varsity')])),
                ('description', models.CharField(max_length=500, null=True, blank=True)),
                ('slug', models.SlugField(null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'teams/', blank=True)),
                ('owner', models.ForeignKey(related_name='team_owner', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('team_id', models.ForeignKey(blank=True, to='teams.Team', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='team_members',
            field=models.ManyToManyField(related_name='members_of_team', null=True, through='teams.TeamMember', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
