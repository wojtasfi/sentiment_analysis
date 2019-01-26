# Generated by Django 2.1.5 on 2019-01-12 18:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('sentiments', '0004_analysispending_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analysispending',
            name='status',
        ),
        migrations.AddField(
            model_name='analysis',
            name='best',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='analysis',
            name='date_of_analysis',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='analysis',
            name='median',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='analysis',
            name='worst',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='analysispending',
            name='date_of_submitting',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='analysis',
            name='mean',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]