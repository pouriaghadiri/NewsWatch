# Generated by Django 2.2.5 on 2020-01-05 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20200105_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='publish_date',
            field=models.DateField(verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='news',
            name='publish_time',
            field=models.TimeField(verbose_name='Publish Time'),
        ),
    ]
