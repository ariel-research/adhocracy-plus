# Generated by Django 3.2.19 on 2024-01-18 11:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("a4_candy_fairvote", "0004_alter_ideachoin_idea"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ideachoin",
            name="missing",
            field=models.FloatField(
                blank=True, default=150, verbose_name="Missing Choins"
            ),
        ),
    ]