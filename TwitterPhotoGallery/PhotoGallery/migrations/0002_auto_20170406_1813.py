# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-06 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PhotoGallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='picture_url',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]