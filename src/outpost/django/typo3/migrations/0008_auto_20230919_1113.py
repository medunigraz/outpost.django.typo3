# Generated by Django 2.2.28 on 2023-09-19 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("typo3", "0007_additional_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsRelatedLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                ("datetime", models.DateTimeField(blank=True, null=True)),
                ("title", models.CharField(blank=True, max_length=256, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("url", models.URLField()),
            ],
            options={
                "db_table": "typo3_news_related_link",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="NewsRelatedMedia",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order",
                    models.PositiveIntegerField(
                        db_index=True, editable=False, verbose_name="order"
                    ),
                ),
                ("datetime", models.DateTimeField(blank=True, null=True)),
                ("title", models.CharField(blank=True, max_length=256, null=True)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "db_table": "typo3_news_related_media",
                "managed": False,
            },
        ),
        migrations.AlterModelOptions(
            name="event",
            options={
                "get_latest_by": "start",
                "managed": False,
                "ordering": ("-start", "-end"),
            },
        ),
    ]
