# Generated by Django 2.2.4 on 2022-06-23 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_one', '0004_auto_20220623_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='fav_wishes',
            field=models.ManyToManyField(related_name='fav', to='app_one.User'),
        ),
    ]
