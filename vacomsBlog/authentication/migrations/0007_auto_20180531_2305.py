# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-31 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_auto_20180531_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=15),
        ),
    ]