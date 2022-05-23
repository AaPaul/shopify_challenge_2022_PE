# Generated by Django 3.2.13 on 2022-05-22 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0003_alter_inventory_warehouse'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('TNT', 'TORONTO'), ('OTT', 'OTTAWA'), ('KAN', 'KANATA'), ('NY', 'NEW YORK'), ('VAN', 'VANCOUVER')], max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='warehouse',
            name='location',
        ),
        migrations.AddField(
            model_name='inventory',
            name='weather',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='apis.city'),
        ),
        migrations.AddField(
            model_name='warehouse',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='apis.city'),
        ),
    ]
