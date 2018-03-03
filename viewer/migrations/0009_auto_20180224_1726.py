# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-24 10:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0008_auto_20150717_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='chord_image',
            field=models.ImageField(default='', upload_to='chords'),
        ),
        migrations.AlterField(
            model_name='song',
            name='chord_url',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='song',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='song',
            name='name',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='view',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='viewer.Song'),
        ),
    ]
