# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import course.models
import django.core.files.storage
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('due_date', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_name', models.CharField(max_length=200, null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('course_code', models.IntegerField(null=True, blank=True)),
                ('course_num', models.CharField(max_length=50, null=True, blank=True)),
                ('course_time', models.CharField(max_length=50, null=True, blank=True)),
                ('course_professor', models.CharField(max_length=100, null=True, blank=True)),
                ('slug', models.SlugField(unique=True, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('course_id', models.ForeignKey(blank=True, to='course.Course', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Syllabus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=350)),
                ('syllabus', models.FileField(storage=django.core.files.storage.FileSystemStorage(location=b'/home/rcmiskin/Desktop/student_g/src/static/protected'), upload_to=course.models.download_loc)),
                ('course', models.ForeignKey(blank=True, to='course.Course', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='course.StudentCourse'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='course',
            field=models.ForeignKey(blank=True, to='course.Course', null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
