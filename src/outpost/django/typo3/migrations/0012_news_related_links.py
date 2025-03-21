# Generated by Django 2.2.28 on 2024-02-29 10:03

from django.db import migrations


class Migration(migrations.Migration):

    ops = [
        (
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_news_related_link";
            """,
            """
            CREATE MATERIALIZED VIEW "public"."typo3_news_related_link" AS
            SELECT
                nl.uid AS id,
                nl.pid AS source_id,
                CASE
                    WHEN nl.sys_language_uid > 0 THEN nl.sys_language_uid
                    ELSE NULL::integer
                END AS language_id,
                CASE nl.tstamp
                    WHEN 0 THEN NULL::timestamp with time zone
                    ELSE to_timestamp(nl.tstamp ::double precision)
                END AS datetime,
                nl.parent AS news_id,
                nl.sorting AS order,
                TRIM(html_unescape(nl.title)) AS title,
                NULLIF(TRIM(html_unescape(nl.description)), '') AS description,
                nl.uri AS url
            FROM typo3.news_links nl
            INNER JOIN typo3.news n ON n.uid = nl.parent
            WHERE
                (n.starttime = 0 OR n.starttime::double precision < date_part('epoch'::text, now())) AND
                (n.endtime = 0 OR n.endtime::double precision > date_part('epoch'::text, now())) AND
                n.deleted = 0 AND
                n.hidden = 0 AND
                n.is_event = 0 AND
                n.t3ver_wsid = 0 AND
                nl.deleted = 0 AND
                nl.hidden = 0 AND
                nl.uri LIKE 'https://%'
            WITH DATA;
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."typo3_news_related_link" AS
            SELECT
                nl.uid AS id,
                nl.pid AS source_id,
                CASE
                    WHEN nl.sys_language_uid > 0 THEN nl.sys_language_uid
                    ELSE NULL::integer
                END AS language_id,
                CASE nl.tstamp
                    WHEN 0 THEN NULL::timestamp with time zone
                    ELSE to_timestamp(nl.tstamp ::double precision)
                END AS datetime,
                nl.parent AS news_id,
                nl.sorting AS order,
                TRIM(html_unescape(nl.title)) AS title,
                NULLIF(TRIM(html_unescape(nl.description)), '') AS description,
                nl.uri AS url
            FROM typo3.news_links nl
            INNER JOIN typo3.news n ON n.uid = nl.parent
            WHERE
                (n.starttime = 0 OR n.starttime < date_part('epoch'::text, now())) AND
                (n.endtime = 0 OR n.endtime > date_part('epoch'::text, now())) AND
                n.deleted = 0 AND
                n.hidden = 0 AND
                n.is_event = 0 AND
                n.t3ver_wsid = 0 AND
                nl.deleted = 0 AND
                nl.hidden = 0
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_news_related_link";
            """,
        ),
    ]

    dependencies = [
        ("typo3", "0011_event_end"),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
