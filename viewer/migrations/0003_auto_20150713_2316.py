# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0002_song_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(default=None, to='viewer.Album'),
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.ForeignKey(default=None, to='viewer.Artist'),
        ),
        migrations.AlterField(
            model_name='song',
            name='chord',
            field=models.ImageField(default=b'', upload_to=b''),
        ),
        migrations.AlterField(
            model_name='song',
            name='code',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='description',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='song',
            name='name',
            field=models.TextField(default=b''),
        ),
    ]
