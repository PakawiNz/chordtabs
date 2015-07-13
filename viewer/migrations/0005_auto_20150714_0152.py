# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0004_auto_20150713_2317'),
    ]

    operations = [
        migrations.RenameField(
            model_name='song',
            old_name='chord',
            new_name='chord_image',
        ),
        migrations.AddField(
            model_name='song',
            name='chord_url',
            field=models.URLField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='song',
            name='viewed',
            field=models.ManyToManyField(to='viewer.User', through='viewer.View'),
            preserve_default=True,
        ),
    ]
