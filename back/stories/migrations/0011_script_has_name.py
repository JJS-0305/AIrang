# Generated by Django 2.2.15 on 2020-10-05 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0010_auto_20201004_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='script',
            name='has_name',
            field=models.BooleanField(default=False),
        ),
    ]
