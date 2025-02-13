# Generated by Django 4.1.2 on 2025-02-13 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("nibble", "0007_rename_belongs_to_comment_card"),
    ]

    operations = [
        migrations.AddField(
            model_name="nibbleprofile",
            name="handle",
            field=models.CharField(default="lmao", max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="comment",
            name="card",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="nibble.card",
            ),
        ),
    ]
