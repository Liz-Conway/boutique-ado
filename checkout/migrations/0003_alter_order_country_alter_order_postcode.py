# Generated by Django 4.0.6 on 2022-08-16 13:44

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ("checkout", "0002_order_original_bag_order_stripe_pid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="country",
            field=django_countries.fields.CountryField(max_length=2),
        ),
        migrations.AlterField(
            model_name="order",
            name="postcode",
            field=models.CharField(default=42424, max_length=20),
            preserve_default=False,
        ),
    ]
