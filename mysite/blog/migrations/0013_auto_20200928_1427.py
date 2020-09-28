# Generated by Django 3.1.1 on 2020-09-28 11:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200928_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 28, 11, 27, 58, 994796, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 28, 11, 27, 58, 992796, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 28, 11, 27, 58, 992796, tzinfo=utc)),
        ),
    ]
