# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-05-25 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_emailverifyrecord_send_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(null=True, upload_to='avatar/%Y/%m', verbose_name='头像'),
        ),
    ]
