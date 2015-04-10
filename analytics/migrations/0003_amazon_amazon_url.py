# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0002_auto_20150324_0731'),
    ]

    operations = [
        migrations.AddField(
            model_name='amazon',
            name='amazon_url',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
    ]
