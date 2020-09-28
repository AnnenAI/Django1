# Generated by Django 3.1.1 on 2020-09-28 11:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200924_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date_added',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 28, 11, 12, 29, 673642, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 28, 11, 12, 29, 671642, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 28, 11, 12, 29, 672642, tzinfo=utc)),
        ),
    ]
