# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-12 12:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='patronymic',
            field=models.CharField(default='', help_text="user's patronymic", max_length=255, verbose_name='patronymic'),
            preserve_default=False,
        ),
    ]
