# Generated by Django 4.1.2 on 2025-02-12 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nibble", "0004_remove_column_label_card_label"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="card",
            name="label",
        ),
        migrations.AddField(
            model_name="card",
            name="label",
            field=models.ManyToManyField(to="nibble.label"),
        ),
    ]
