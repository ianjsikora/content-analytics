# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amazon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(default=b'movie', max_length=6, choices=[(b'movie', b'Movie'), (b'series', b'Series')])),
                ('season', models.IntegerField(null=True)),
                ('amazon_rating', models.IntegerField(null=True)),
                ('imdb_id', models.CharField(max_length=30, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('imdb_id', models.CharField(max_length=30, null=True)),
                ('imdb_url', models.URLField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('release_date', models.DateField(null=True)),
                ('release_year', models.IntegerField(null=True)),
                ('runtime', models.IntegerField(null=True)),
                ('mpaa_rating', models.CharField(max_length=10)),
                ('budget', models.IntegerField(null=True)),
                ('revenue', models.IntegerField(null=True)),
                ('synopsis', models.TextField(null=True)),
                ('imdb_rating', models.FloatField(null=True)),
                ('poster', models.URLField(null=True)),
                ('imdb_id', models.CharField(max_length=30, null=True)),
                ('imdb_url', models.URLField(null=True)),
                ('amazon', models.ForeignKey(to='analytics.Amazon')),
                ('characters', models.ManyToManyField(to='analytics.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('imdb_id', models.CharField(max_length=30, null=True)),
                ('imdb_url', models.URLField(null=True)),
                ('headshot', models.URLField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SourceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='type',
            field=models.ManyToManyField(to='analytics.PersonType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='content_type',
            field=models.ForeignKey(to='analytics.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='director',
            field=models.ManyToManyField(related_name='director', to='analytics.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='genre',
            field=models.ManyToManyField(to='analytics.Genre'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='keywords',
            field=models.ManyToManyField(to='analytics.Keyword'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='source_types',
            field=models.ManyToManyField(to='analytics.SourceType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='writer',
            field=models.ManyToManyField(related_name='writer', to='analytics.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='actor',
            field=models.ManyToManyField(to='analytics.Person'),
            preserve_default=True,
        ),
    ]
