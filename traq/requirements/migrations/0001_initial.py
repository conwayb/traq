# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('approved_on', models.DateTimeField(null=True, blank=True)),
                ('approved_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='requirements_approved', blank=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
                ('milestone', models.ForeignKey(to='projects.Milestone', null=True, blank=True)),
                ('modified_by', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='+')),
                ('project', models.ForeignKey(to='projects.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
