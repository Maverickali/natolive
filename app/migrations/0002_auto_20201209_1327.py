# Generated by Django 2.2.10 on 2020-12-09 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='injections',
            name='injection_amount',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='injections',
            name='update_date',
            field=models.DateTimeField(null=True, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='injections',
            name='updated_by',
            field=models.CharField(max_length=200, null=True),
        ),
    ]