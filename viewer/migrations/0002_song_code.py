# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='code',
            field=models.IntegerField(default=None, unique=True),
            preserve_default=False,
        ),
    ]
