# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0003_auto_20150713_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(default=None, to='viewer.Album', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.ForeignKey(default=None, to='viewer.Artist', null=True),
        ),
    ]
