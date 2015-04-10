# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_imdb'),
    ]

    operations = [
        migrations.CreateModel(
            name='Viki',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(default=b'movie', max_length=6, choices=[(b'movie', b'Movie'), (b'series', b'Series')])),
                ('country', models.CharField(max_length=50, null=True)),
                ('viki_url', models.URLField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
