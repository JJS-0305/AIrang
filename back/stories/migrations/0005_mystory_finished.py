# Generated by Django 2.2.15 on 2020-09-26 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0004_merge_20200924_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='mystory',
            name='finished',
            field=models.BooleanField(default=False),
        ),
    ]
