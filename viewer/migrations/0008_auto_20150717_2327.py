# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0007_auto_20150714_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='view',
            name='user',
            field=models.ForeignKey(to='viewer.User', null=True),
        ),
    ]
