# Generated by Django 3.2 on 2021-04-17 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
