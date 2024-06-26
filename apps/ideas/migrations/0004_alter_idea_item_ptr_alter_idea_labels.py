# Generated by Django 4.0 on 2024-02-07 14:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("a4modules", "0008_alter_module_blueprint_type"),
        ("a4labels", "0003_labelalias"),
        ("a4_candy_ideas", "0003_alter_idea_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="idea",
            name="item_ptr",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                primary_key=True,
                related_name="%(app_label)s_%(class)s",
                serialize=False,
                to="a4modules.item",
            ),
        ),
        migrations.AlterField(
            model_name="idea",
            name="labels",
            field=models.ManyToManyField(
                related_name="%(app_label)s_%(class)s_label",
                to="a4labels.Label",
                verbose_name="Labels",
            ),
        ),
    ]
