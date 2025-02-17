# Generated by Django 2.2.28 on 2023-04-06 08:30

from django.db import migrations


class Migration(migrations.Migration):

    ops = [
        (
            """
            DROP INDEX IF EXISTS "typo3_event_id_idx";
            """,
            """
            CREATE UNIQUE INDEX "typo3_event_id_idx" ON "public"."typo3_event" USING btree (id);
            """,
        ),
        (
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_event";
            """,
            """
            CREATE MATERIALIZED VIEW "public"."typo3_event" AS
            SELECT
                n.uid AS id,
                n.pid AS source_id,
                CASE
                    n.full_day
                WHEN
                    1
                THEN
                    to_timestamp(n.datetime)::date + '00:00:00'::INTERVAL
                ELSE
                    to_timestamp(n.datetime)
                END AS START,
                CASE
                    n.full_day
                WHEN
                    1
                THEN
                    to_timestamp(n.event_end)::date + '24:00:00'::INTERVAL
                ELSE
                    to_timestamp(n.event_end)
                END AS "end",
                n.full_day::int::boolean AS allday,
                html_unescape(n.title) AS title,
                NULLIF(BTRIM(n.organizer_simple, ' '), '') AS organizer,
                NULLIF(BTRIM(n.location_simple, ' '), '') AS location,
                html_unescape(n.teaser) AS teaser,
                html_unescape(n.bodytext) AS body,
                regexp_split_to_array(NULLIF(TRIM(n.keywords), ''), '\s*,\s*') AS keywords,
                NULLIF(TRIM(n.description), '') AS description,
                CASE WHEN
                    n.sys_language_uid > 0
                THEN
                    n.sys_language_uid
                ELSE
                    NULL
                END AS language_id,
                n.register::int::boolean AS register,
                CASE WHEN
                    n.registration_end > 0
                THEN
                    to_timestamp(n.registration_end)
                ELSE
                    NULL
                END AS registration_end,
                n.attendingfees::int::boolean AS attending_fees,
                NULLIF(TRIM(n.attendingfees_info), '') AS attending_fees_info,
                NULLIF(BTRIM(n.www, ' '), '') AS link,
                CASE WHEN
                    n.dfppoints > 0
                THEN
                    n.dfppoints
                ELSE
                    NULL
                END AS dfp_points,
                NULLIF(BTRIM(n.contact_name, ' '), '') AS contact,
                NULLIF(BTRIM(n.contact_email, ' '), '') AS email,
                to_timestamp(n.tstamp) AS last_modified
            FROM
                typo3.news AS n
            WHERE
                n.datetime <> 0
                AND
                n.event_end <> 0
                AND
                (
                    n.starttime = 0
                    OR
                    n.starttime > date_part('epoch'::text, now())
                )
                AND
                (
                    CASE
                        n.full_day
                    WHEN
                        1
                    THEN
                        n.event_end + 86400
                    ELSE
                        n.event_end
                    END
                ) > date_part('epoch'::text, now())
                AND
                n.deleted = 0
                AND
                n.hidden = 0
                AND
                n.is_event = 1
            WITH DATA;
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."typo3_event" AS
            SELECT
                n.uid AS id,
                n.pid AS source_id,
                CASE
                    n.full_day
                WHEN
                    1
                THEN
                    to_timestamp(n.datetime)::date + '00:00:00'::INTERVAL
                ELSE
                    to_timestamp(n.datetime)
                END AS START,
                CASE
                    n.full_day
                WHEN
                    1
                THEN
                    to_timestamp(n.event_end)::date + '24:00:00'::INTERVAL
                ELSE
                    to_timestamp(n.event_end)
                END AS "end",
                n.full_day::int::boolean AS allday,
                html_unescape(n.title) AS title,
                NULLIF(BTRIM(n.organizer_simple, ' '), '') AS organizer,
                NULLIF(BTRIM(n.location_simple, ' '), '') AS location,
                html_unescape(n.teaser) AS teaser,
                html_unescape(n.bodytext) AS body,
                regexp_split_to_array(NULLIF(TRIM(n.keywords), ''), '\s*,\s*') AS keywords,
                NULLIF(TRIM(n.description), '') AS description,
                CASE WHEN
                    n.sys_language_uid > 0
                THEN
                    n.sys_language_uid
                ELSE
                    NULL
                END AS language_id,
                n.register::int::boolean AS register,
                CASE WHEN
                    n.registration_end > 0
                THEN
                    to_timestamp(n.registration_end)
                ELSE
                    NULL
                END AS registration_end,
                n.attendingfees::int::boolean AS attending_fees,
                NULLIF(TRIM(n.attendingfees_info), '') AS attending_fees_info,
                NULLIF(BTRIM(n.www, ' '), '') AS link,
                CASE WHEN
                    n.dfppoints > 0
                THEN
                    n.dfppoints
                ELSE
                    NULL
                END AS dfp_points,
                NULLIF(BTRIM(n.contact_name, ' '), '') AS contact,
                NULLIF(BTRIM(n.contact_email, ' '), '') AS email,
                to_timestamp(n.tstamp) AS last_modified
            FROM
                typo3.news AS n
            WHERE
                n.datetime <> 0
                AND
                n.event_end <> 0
                AND
                (
                    n.starttime = 0
                    OR
                    n.starttime > date_part('epoch'::text, now())
                )
                AND
                (
                    CASE
                        n.full_day
                    WHEN
                        1
                    THEN
                        n.event_end + 86400
                    ELSE
                        n.event_end
                    END
                ) > date_part('epoch'::text, now())
                AND
                n.deleted = 0
                AND
                n.hidden = 0
                AND
                n.is_event = 1
                AND
                n.t3ver_wsid = 0
            WITH DATA;
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."typo3_event";
            """,
        ),
        (
            """
            CREATE UNIQUE INDEX "typo3_event_id_idx" ON "public"."typo3_event" USING btree (id);
            """,
            """
            DROP INDEX IF EXISTS "typo3_event_id_idx";
            """,
        ),
    ]

    dependencies = [
        ("typo3", "0009_newsmedia_preview"),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
