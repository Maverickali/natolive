# Generated by Django 2.2.10 on 2021-02-22 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Daily_Report',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('opening_bal', models.FloatField(default=0.0)),
                ('total_collections', models.FloatField(default=0.0)),
                ('total_processing_fees', models.FloatField(default=0.0)),
                ('total_disbursed', models.FloatField(default=0.0)),
                ('injection_in', models.FloatField(default=0.0)),
                ('injection_out', models.FloatField(default=0.0)),
                ('total_banked', models.FloatField(default=0.0)),
                ('total_expenses_daily', models.FloatField(default=0.0)),
                ('closing_bal', models.FloatField(default=0.0)),
                ('previous_closing_portfolio', models.FloatField(default=0.0)),
                ('total_clients_disbursed', models.IntegerField(default=False)),
                ('activity_date', models.DateField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Potential_Customers',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(default=False, max_length=100)),
                ('last_name', models.CharField(default=False, max_length=100)),
                ('contact', models.CharField(default=False, max_length=100)),
                ('amount_desired', models.FloatField(default=False)),
                ('client_type', models.CharField(default=False, max_length=100)),
                ('desire_date', models.DateField(default=False)),
                ('turn_over', models.CharField(default='potential_cilent', max_length=100, null=True)),
                ('business_type', models.CharField(default=False, max_length=100)),
                ('business_location', models.CharField(default=False, max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Disbursements',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount_disbursed', models.FloatField(default=0.0)),
                ('disbursed_date', models.DateField(default=False)),
                ('id_number', models.IntegerField(default=0.0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Branch')),
                ('customer_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Potential_Customers')),
            ],
        ),
    ]
