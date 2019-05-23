# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-10 09:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    forward = [
        """
        CREATE UNIQUE INDEX typo3_event_id_idx ON "public"."typo3_event" ("id");
        """,
        """
        CREATE UNIQUE INDEX typo3_news_id_idx ON "public"."typo3_news" ("id");
        """,
    ]

    reverse = [
        """
        DROP INDEX IF EXISTS typo3_news_id_idx;
        """,
        """
        DROP INDEX IF EXISTS typo3_event_id_idx;
        """,
    ]

    dependencies = [("typo3", "0006_newscategory")]

    operations = [migrations.RunSQL(forward, reverse)]
