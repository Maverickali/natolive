# Generated by Django 2.2.10 on 2020-12-11 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20201211_1832'),
    ]

    operations = [
        migrations.RenameField(
            model_name='injections',
            old_name='branch',
            new_name='branch_name',
        ),
        migrations.RenameField(
            model_name='injections',
            old_name='new_customers_amount',
            new_name='new_customer_amount',
        ),
        migrations.RenameField(
            model_name='injections',
            old_name='new_customers',
            new_name='new_customer_numbers',
        ),
        migrations.RenameField(
            model_name='injections',
            old_name='repeat_customers_amount',
            new_name='repeat_customer_amount',
        ),
        migrations.RenameField(
            model_name='injections',
            old_name='repeat_customers',
            new_name='repeat_customer_numbers',
        ),
    ]
