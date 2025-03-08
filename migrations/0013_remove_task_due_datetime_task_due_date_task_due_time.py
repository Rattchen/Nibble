# Generated by Django 4.1.2 on 2025-03-08 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nibble", "0012_alter_task_priority_alter_tasktype_icon"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="task",
            name="due_datetime",
        ),
        migrations.AddField(
            model_name="task",
            name="due_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="task",
            name="due_time",
            field=models.TimeField(blank=True, null=True),
        ),
    ]
