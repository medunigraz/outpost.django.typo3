# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-31 07:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    forward = [
        """
        CREATE UNIQUE INDEX typo3_eventmedia_id_idx ON "public"."typo3_eventmedia" ("id");
        """,
        """
        CREATE UNIQUE INDEX typo3_newsmedia_id_idx ON "public"."typo3_newsmedia" ("id");
        """,
        """
        CREATE INDEX typo3_eventmedia_event_id_idx ON "public"."typo3_eventmedia" ("event_id");
        """,
        """
        CREATE INDEX typo3_newsmedia_news_id_idx ON "public"."typo3_newsmedia" ("news_id");
        """,
        """
        CREATE INDEX typo3_eventmedia_mimetype_idx ON "public"."typo3_eventmedia" ("mimetype");
        """,
        """
        CREATE INDEX typo3_newsmedia_mimetype_idx ON "public"."typo3_newsmedia" ("mimetype");
        """,
    ]

    reverse = [
        """
        DROP INDEX IF EXISTS typo3_newsmedia_mimetype_idx;
        """,
        """
        DROP INDEX IF EXISTS typo3_eventmedia_mimetype_idx;
        """,
        """
        DROP INDEX IF EXISTS typo3_newsmedia_news_id_idx;
        """,
        """
        DROP INDEX IF EXISTS typo3_eventmedia_event_id_idx;
        """,
        """
        DROP INDEX IF EXISTS typo3_newsmedia_id_idx;
        """,
        """
        DROP INDEX IF EXISTS typo3_eventmedia_id_idx;
        """,
    ]

    dependencies = [("typo3", "0011_eventmedia")]

    operations = [migrations.RunSQL(forward, reverse)]
