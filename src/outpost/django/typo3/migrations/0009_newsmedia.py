# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-30 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typo3', '0008_news_media'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsMedia',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('alternative', models.TextField(blank=True, null=True)),
                ('url', models.URLField()),
                ('mimetype', models.CharField(blank=True, max_length=256, null=True)),
                ('filename', models.CharField(blank=True, max_length=256, null=True)),
                ('size', models.PositiveIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'typo3_newsmedia',
                'managed': False,
            },
        ),
    ]
