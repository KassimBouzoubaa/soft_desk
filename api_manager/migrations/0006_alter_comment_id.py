# Generated by Django 5.0.4 on 2024-04-28 02:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_manager", "0005_alter_comment_id_delete_ok"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
