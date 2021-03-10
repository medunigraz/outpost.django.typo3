# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-18 18:26
from __future__ import unicode_literals

from django.db import migrations

from django.conf import settings


class Migration(migrations.Migration):

    forward = [
        """
        CREATE MATERIALIZED VIEW "public"."typo3_media" AS SELECT
            uid AS id,
            format('{base}%s', identifier) AS url,
            mime_type AS mimetype,
            name AS filename,
            size AS size
        FROM
            typo3.file
        """.format(
            base=settings.TYPO3_FILEADMIN_URL
        ),
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_newsmedia";
        """,
        """
        CREATE MATERIALIZED VIEW "public"."typo3_newsmedia" AS SELECT
            r.uid AS id,
            r.uid_local AS media_id,
            r.uid_foreign AS news_id,
            CASE trim(both ' ' from r.title) WHEN '' THEN NULL ELSE trim(both ' ' from r.title) END AS title,
            CASE trim(both ' ' from r.description) WHEN '' THEN NULL ELSE trim(both ' ' from r.description) END AS description,
            CASE trim(both ' ' from r.alternative) WHEN '' THEN NULL ELSE trim(both ' ' from r.alternative) END AS alternative,
            CASE WHEN r.sys_language_uid <= 0 THEN NULL ELSE r.sys_language_uid END AS language_id,
            r.sorting AS order,
            r.showinpreview::boolean AS preview
        FROM
            typo3.news n,
            typo3.file_reference r
        WHERE
            r.tablenames = 'tx_news_domain_model_news' AND
            r.table_local = 'sys_file' AND
            r.fieldname = 'fal_media' AND
            r.uid_foreign = n.uid AND
            n.deleted = 0 AND
            n.hidden = 0 AND
            r.deleted = 0 AND
            r.hidden = 0
        """.format(
            base=settings.TYPO3_FILEADMIN_URL
        ),
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_eventmedia";
        """,
        """
        CREATE MATERIALIZED VIEW "public"."typo3_eventmedia" AS  SELECT
            r.uid AS id,
            r.uid_local AS media_id,
            r.uid_foreign AS event_id,
            CASE trim(both ' ' from r.title) WHEN '' THEN NULL ELSE trim(both ' ' from r.title) END AS title,
            CASE trim(both ' ' from r.description) WHEN '' THEN NULL ELSE trim(both ' ' from r.description) END AS description,
            CASE trim(both ' ' from r.alternative) WHEN '' THEN NULL ELSE trim(both ' ' from r.alternative) END AS alternative,
            CASE WHEN r.sys_language_uid <= 0 THEN NULL ELSE r.sys_language_uid END AS language_id,
            r.sorting AS order,
            r.showinpreview::boolean AS preview
        FROM
            typo3.event e,
            typo3.file_reference r
        WHERE
            r.tablenames = 'tx_cal_event' AND
            r.table_local = 'sys_file' AND
            r.fieldname IN ('attachment', 'image') AND
            r.uid_foreign = e.uid AND
            e.deleted = 0 AND
            e.hidden = 0 AND
            r.deleted = 0 AND
            r.hidden = 0
        """.format(
            base=settings.TYPO3_FILEADMIN_URL
        ),
    ]
    reverse = [
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_eventmedia";
        """,
        """
        CREATE MATERIALIZED VIEW "public"."typo3_eventmedia" AS  SELECT
            r.uid AS id,
            f.uid AS media_id,
            e.uid AS event_id,
            CASE trim(both ' ' from r.title) WHEN '' THEN NULL ELSE trim(both ' ' from r.title) END AS title,
            CASE trim(both ' ' from r.description) WHEN '' THEN NULL ELSE trim(both ' ' from r.description) END AS description,
            CASE trim(both ' ' from r.alternative) WHEN '' THEN NULL ELSE trim(both ' ' from r.alternative) END AS alternative,
            CASE WHEN r.sys_language_uid <= 0 THEN NULL ELSE r.sys_language_uid END AS language_id,
            format('{base}%s', f.identifier) AS url,
            f.mime_type AS mimetype,
            f.name AS filename,
            f.size AS size,
            r.sorting AS order
        FROM
            typo3.event e,
            typo3.file_reference r,
            typo3.file f
        WHERE
            r.tablenames = 'tx_cal_event' AND
            r.table_local = 'sys_file' AND
            r.fieldname IN ('attachment', 'image') AND
            r.uid_foreign = e.uid AND
            f.uid = r.uid_local AND
            e.deleted = 0 AND
            e.hidden = 0 AND
            r.deleted = 0 AND
            r.hidden = 0
        """.format(
            base=settings.TYPO3_FILEADMIN_URL
        ),
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_newsmedia";
        """,
        """
        CREATE MATERIALIZED VIEW "public"."typo3_newsmedia" AS SELECT
            r.uid AS id,
            f.uid AS media_id,
            n.uid AS news_id,
            CASE trim(both ' ' from r.title) WHEN '' THEN NULL ELSE trim(both ' ' from r.title) END AS title,
            CASE trim(both ' ' from r.description) WHEN '' THEN NULL ELSE trim(both ' ' from r.description) END AS description,
            CASE trim(both ' ' from r.alternative) WHEN '' THEN NULL ELSE trim(both ' ' from r.alternative) END AS alternative,
            CASE WHEN r.sys_language_uid <= 0 THEN NULL ELSE r.sys_language_uid END AS language_id,
            format('{base}%s', f.identifier) AS url,
            f.mime_type AS mimetype,
            f.name AS filename,
            f.size AS size,
            r.sorting AS order
        FROM
            typo3.news n,
            typo3.file_reference r,
            typo3.file f
        WHERE
            r.tablenames = 'tx_news_domain_model_news' AND
            r.table_local = 'sys_file' AND
            r.fieldname = 'fal_media' AND
            r.uid_foreign = n.uid AND
            f.uid = r.uid_local AND
            n.deleted = 0 AND
            n.hidden = 0 AND
            r.deleted = 0 AND
            r.hidden = 0
        """.format(
            base=settings.TYPO3_FILEADMIN_URL
        ),
        """
        DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_media";
        """,
    ]

    dependencies = [("typo3", "0016_eventcategory")]

    operations = [migrations.RunSQL(forward, reverse)]
