# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('route', '0002_auto_20150123_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='description',
            field=models.CharField(max_length=10000, null=True, blank=True),
            preserve_default=True,
        ),
    ]
