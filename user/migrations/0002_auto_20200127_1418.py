# Generated by Django 3.0.2 on 2020-01-28 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='user',
        ),
        migrations.AddField(
            model_name='person',
            name='first_name',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='username',
            field=models.CharField(default=1, max_length=300),
            preserve_default=False,
        ),
    ]
