# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-14 09:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20171114_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historytrade',
            name='price',
            field=models.FloatField(default=-1),
        ),
    ]
