# Generated by Django 3.1 on 2021-08-12 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0004_auto_20210811_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
