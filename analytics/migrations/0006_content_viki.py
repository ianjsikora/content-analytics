# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_viki'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='viki',
            field=models.ForeignKey(to='analytics.Viki', null=True),
            preserve_default=True,
        ),
    ]
