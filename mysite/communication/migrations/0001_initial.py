# Generated by Django 3.1.1 on 2020-09-28 13:59

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialogue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_message_date', models.DateTimeField(default=datetime.datetime(2020, 9, 28, 13, 59, 1, 175124, tzinfo=utc))),
            ],
            options={
                'ordering': ['-last_message_date'],
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dialogue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='communication.dialogue')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_sending', models.DateTimeField(default=datetime.datetime(2020, 9, 28, 13, 59, 1, 176124, tzinfo=utc))),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('dialogue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='communication.dialogue')),
            ],
            options={
                'ordering': ['-date_sending'],
            },
        ),
    ]
