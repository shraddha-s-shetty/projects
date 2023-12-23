# Generated by Django 5.0 on 2023-12-23 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("second_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Users",
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
                ("first_name", models.CharField(max_length=264)),
                ("last_name", models.CharField(max_length=264)),
                ("email", models.CharField(max_length=264)),
            ],
        ),
    ]