# Generated by Django 5.0.4 on 2024-04-15 22:18

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("description", models.TextField(blank=True)),
                ("created_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Contributor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "statut",
                    models.CharField(
                        choices=[
                            ("to_do", "To Do"),
                            ("in_progress", "In Progress"),
                            ("finished", "Finished"),
                        ],
                        default="to_do",
                        max_length=20,
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            ("low", "LOW"),
                            ("medium", "MEDIUM"),
                            ("high", "HIGH"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "balise",
                    models.CharField(
                        choices=[
                            ("bug", "BUG"),
                            ("feature", "FEATURE"),
                            ("task", "TASK"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                (
                    "project_type",
                    models.CharField(
                        choices=[
                            ("front-end", "Front-end"),
                            ("backend", "Backend"),
                            ("iOS", "iOS"),
                            ("android", "Android"),
                        ],
                        max_length=20,
                    ),
                ),
                ("created_time", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]