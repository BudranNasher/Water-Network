# Generated by Django 4.1.7 on 2023-02-25 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_point_tree'),
    ]

    operations = [
        migrations.AddField(
            model_name='valve',
            name='soft_delete',
            field=models.BooleanField(default=False),
        ),
    ]
