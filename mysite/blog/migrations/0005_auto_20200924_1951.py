# Generated by Django 3.1.1 on 2020-09-24 16:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200924_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 24, 16, 51, 49, 341374, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 24, 16, 51, 49, 339374, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 24, 16, 51, 49, 339374, tzinfo=utc)),
        ),
    ]
