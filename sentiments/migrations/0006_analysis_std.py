# Generated by Django 2.1.5 on 2019-01-12 18:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sentiments', '0005_auto_20190112_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='std',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
