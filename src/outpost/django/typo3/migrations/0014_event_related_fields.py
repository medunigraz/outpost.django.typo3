# Generated by Django 2.2.28 on 2024-04-08 12:54

from django.db import migrations


class Migration(migrations.Migration):

    ops = [
        (
            """
            CREATE MATERIALIZED VIEW "public"."typo3_event_related_link" AS
            SELECT
                nl.uid AS id,
                nl.pid AS source_id,
                CASE
                    WHEN nl.sys_language_uid > 0 THEN nl.sys_language_uid::integer
                    ELSE NULL::integer
                END AS language_id,
                CASE nl.tstamp
                    WHEN 0 THEN NULL::timestamp with time zone
                    ELSE to_timestamp(nl.tstamp::double precision)
                END AS datetime,
                nl.parent AS event_id,
                nl.sorting AS "order",
                btrim(html_unescape(nl.title::text)) AS title,
                NULLIF(btrim(html_unescape(nl.description)), ''::text) AS description,
                nl.uri AS url
            FROM typo3.news_links nl
            JOIN typo3.news n ON n.uid = nl.parent
            WHERE
                (
                    n.starttime = 0 OR
                    n.starttime::double precision < date_part('epoch'::text, now())
                ) AND
                (
                    n.endtime = 0 OR
                    n.endtime::double precision > date_part('epoch'::text, now())
                ) AND
                n.deleted = 0 AND
                n.hidden = 0 AND
                n.is_event = 1 AND
                n.t3ver_wsid = 0 AND
                nl.deleted = 0 AND
                nl.hidden = 0
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_event_related_link";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."typo3_event_related_media" AS
            SELECT
                fr.uid as id,
                fr.pid as source_id,
                CASE
                    WHEN fr.sys_language_uid > 0 THEN fr.sys_language_uid::integer
                    ELSE NULL::integer
                END AS language_id,
                CASE fr.tstamp
                    WHEN 0 THEN NULL::timestamp with time zone
                    ELSE to_timestamp(fr.tstamp::double precision)
                END AS datetime,
                fr.uid_local as media_id,
                fr.uid_foreign as event_id,
                fr.sorting_foreign as order,
                NULLIF(TRIM(fr.title), '') as title,
                NULLIF(TRIM(fr.description), '') as description
            FROM typo3.file_reference fr
                inner join typo3.news n on fr.uid_foreign = n.uid
                inner join typo3.file f on f.uid = fr.uid_local
            where
                fr.tablenames = 'tx_news_domain_model_news' and
                fr.fieldname = 'fal_related_files' and
                fr.table_local= 'sys_file' and
                (
                    n.starttime = 0 OR
                    n.starttime::double precision < date_part('epoch'::text, now())
                ) AND
                (
                    n.endtime = 0 OR
                    n.endtime::double precision > date_part('epoch'::text, now())
                ) AND
                n.deleted = 0 AND
                n.hidden = 0 AND
                n.is_event = 1 AND
                n.t3ver_wsid = 0 AND
                f.storage > 0 AND
                f.missing = 0
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_event_related_media";
            """,
        ),
        (
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_news_related_media";
            """,
            """
            CREATE MATERIALIZED VIEW public.typo3_news_related_media AS
            SELECT
                nl.uid AS id,
                nl.pid AS source_id,
                    CASE
                        WHEN nl.sys_language_uid > 0 THEN nl.sys_language_uid::integer
                        ELSE NULL::integer
                    END AS language_id,
                    CASE nl.tstamp
                        WHEN 0 THEN NULL::timestamp with time zone
                        ELSE to_timestamp(nl.tstamp::double precision)
                    END AS datetime,
                nl.parent AS news_id,
                nl.sorting AS "order",
                btrim(html_unescape(nl.title::text)) AS title,
                NULLIF(btrim(html_unescape(nl.description)), ''::text) AS description,
                f.uid AS media_id
            FROM typo3.news_links nl
                JOIN typo3.news n ON n.uid = nl.parent
                JOIN typo3.file f ON f.uid =
                    CASE
                        WHEN nl.uri ^@ 'file:'::text THEN "substring"(nl.uri, '^file:(\d+)'::text)
                        WHEN nl.uri ^@ 't3://file?uid='::text THEN "substring"(nl.uri, '^t3://file\?uid=(\d+)'::text)
                        ELSE NULL::text
                    END::integer
            WHERE
                (
                    n.starttime = 0 OR
                    n.starttime::double precision < date_part('epoch'::text, now())
                ) AND
                (
                    n.endtime = 0 OR
                    n.endtime::double precision > date_part('epoch'::text, now())
                ) AND
                n.deleted = 0 AND
                n.hidden = 0 AND
                n.is_event = 0 AND
                n.t3ver_wsid = 0 AND
                f.storage > 0 AND
                f.missing = 0 AND
                nl.deleted = 0 AND
                nl.hidden = 0 AND
                (
                    nl.uri LIKE 'file:%' OR
                    nl.uri LIKE 't3://file?uid=%'
                )
            WITH DATA;
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."typo3_news_related_media" AS
            SELECT
                fr.uid as id,
                fr.pid as source_id,
                CASE
                    WHEN fr.sys_language_uid > 0 THEN fr.sys_language_uid::integer
                    ELSE NULL::integer
                END AS language_id,
                CASE fr.tstamp
                    WHEN 0 THEN NULL::timestamp with time zone
                    ELSE to_timestamp(fr.tstamp::double precision)
                END AS datetime,
                fr.uid_local as media_id,
                fr.uid_foreign as news_id,
                fr.sorting_foreign as order,
                NULLIF(TRIM(fr.title), '') as title,
                NULLIF(TRIM(fr.description), '') as description
            FROM typo3.file_reference fr
                inner join typo3.news n on fr.uid_foreign = n.uid
                inner join typo3.file f on f.uid = fr.uid_local
            where
                fr.tablenames = 'tx_news_domain_model_news' and
                fr.fieldname = 'fal_related_files' and
                fr.table_local= 'sys_file' and
                (
                    n.starttime = 0 OR
                    n.starttime::double precision < date_part('epoch'::text, now())
                ) AND
                (
                    n.endtime = 0 OR
                    n.endtime::double precision > date_part('epoch'::text, now())
                ) AND
                n.deleted = 0 AND
                n.hidden = 0 AND
                n.is_event = 0 AND
                n.t3ver_wsid = 0 AND
                f.storage > 0 AND
                f.missing = 0
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_news_related_media";
            """,
        ),
    ]

    dependencies = [
        ("typo3", "0013_gallery_contactbox"),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]