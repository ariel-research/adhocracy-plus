# Generated by Django 3.2.10 on 2022-01-11 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('a4_candy_polls', '0004_delete_choice_question_vote'),
    ]

    operations = [
        migrations.DeleteModel(
            name='APlusPoll',
        ),
    ]