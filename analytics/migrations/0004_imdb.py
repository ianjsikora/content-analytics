# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_amazon_amazon_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='IMDb',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(default=b'movie', max_length=6, choices=[(b'movie', b'Movie'), (b'series', b'Series')])),
                ('release_year', models.IntegerField(null=True)),
                ('episodes', models.IntegerField(null=True)),
                ('imdb_streaming_url', models.URLField(null=True)),
                ('imdb_id', models.CharField(max_length=30, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
