# Generated by Django 4.2 on 2023-04-20 05:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("traits", "0006_rename_name_trait_trait_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="trait",
            old_name="trait_name",
            new_name="name",
        ),
    ]
