# Generated by Django 3.2.7 on 2021-09-27 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_newuser_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='photo',
            field=models.IntegerField(choices=[(1, 'Default'), (2, 'Girl'), (3, 'Boy')], default=1),
        ),
    ]
