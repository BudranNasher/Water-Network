# Generated by Django 4.1.2 on 2023-02-21 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_point_valve'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='distance',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]