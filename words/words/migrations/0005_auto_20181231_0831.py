# Generated by Django 2.1.4 on 2018-12-31 00:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('words', '0004_auto_20180407_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_time',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now, verbose_name='Review Time'),
        ),
    ]
