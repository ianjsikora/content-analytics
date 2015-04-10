# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Netflix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(default=b'movie', max_length=6, choices=[(b'movie', b'Movie'), (b'series', b'Series')])),
                ('season', models.IntegerField(null=True)),
                ('release_year', models.IntegerField(null=True)),
                ('netflix_rating', models.IntegerField(null=True)),
                ('netflix_url', models.URLField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='amazon',
            name='release_year',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='netflix',
            field=models.ForeignKey(to='analytics.Netflix', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='content',
            name='amazon',
            field=models.ForeignKey(to='analytics.Amazon', null=True),
            preserve_default=True,
        ),
    ]
