# Generated by Django 3.2 on 2021-05-16 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_potential_customers_loan_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='rm_collection_sheets',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.potential_customers'),
        ),
    ]