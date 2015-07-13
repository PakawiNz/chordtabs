# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.TextField()),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.TextField()),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('chord', models.ImageField(upload_to=b'')),
                ('album', models.ForeignKey(to='viewer.Album')),
                ('artist', models.ForeignKey(to='viewer.Artist')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.EmailField(unique=True, max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('displayname', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('count', models.IntegerField(default=0)),
                ('isFavorite', models.BooleanField(default=False)),
                ('song', models.ForeignKey(to='viewer.Song')),
                ('user', models.ForeignKey(to='viewer.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
