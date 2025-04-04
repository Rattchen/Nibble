# Generated by Django 4.1.2 on 2025-02-18 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("nibble", "0009_alter_nibbleprofile_bio_alter_nibbleprofile_handle"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="assigned_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_tasks",
                to="nibble.nibbleprofile",
            ),
        ),
    ]
