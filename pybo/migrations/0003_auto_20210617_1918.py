# Generated by Django 2.2.5 on 2021-06-17 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0002_auto_20210616_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='backAngCheck',
            field=models.IntegerField(default=0),
        ),
    ]