# Generated by Django 2.2.5 on 2021-06-17 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0004_question_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='backAngCheck',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=10),
        ),
    ]