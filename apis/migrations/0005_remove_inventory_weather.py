# Generated by Django 3.2.13 on 2022-05-23 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0004_auto_20220522_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inventory',
            name='weather',
        ),
    ]