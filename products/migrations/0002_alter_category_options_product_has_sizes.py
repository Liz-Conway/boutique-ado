# Generated by Django 4.0.6 on 2022-07-16 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
        migrations.AddField(
            model_name="product",
            name="has_sizes",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
