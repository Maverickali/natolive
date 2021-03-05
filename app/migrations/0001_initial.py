# Generated by Django 2.2.10 on 2021-02-23 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # migrations.CreateModel(
        #     name='Branch',
        #     fields=[
        #         ('id', models.BigAutoField(primary_key=True, serialize=False)),
        #         ('branch_name', models.CharField(max_length=50, unique=True)),
        #         ('creation_date', models.DateTimeField(auto_now_add=True)),
        #         ('created_by', models.CharField(max_length=50)),
        #     ],
        # ),
        migrations.CreateModel(
            name='Daily_Report',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('opening_bal', models.FloatField(default=0.0)),
                ('total_collections', models.FloatField(default=0.0, null=True)),
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
                ('branch_id', models.IntegerField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Injections',
            fields=[
                ('record_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('branch_name', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('cash_forward', models.FloatField(default=0.0)),
                ('repeat_customer_numbers', models.IntegerField(default=0)),
                ('new_customer_numbers', models.IntegerField(default=0)),
                ('repeat_customer_amount', models.FloatField(default=0.0)),
                ('new_customer_amount', models.FloatField(default=0.0)),
                ('cash_reserve_need', models.FloatField(default=0.0)),
                ('injection_amount', models.FloatField(default=0.0, null=True)),
                ('injection_status', models.BooleanField(default=False)),
                ('injection_authorization', models.CharField(default='False', max_length=10)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(max_length=50)),
                ('update_date', models.DateTimeField(auto_now=True, null=True)),
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
                ('branch_id', models.IntegerField(default=False)),
                ('desire_date', models.DateField(default=False)),
                ('turn_over', models.CharField(default='potential_cilent', max_length=100, null=True)),
                ('business_type', models.CharField(default=False, max_length=100)),
                ('business_location', models.CharField(default=False, max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RM_Collection_Sheets',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(default=False, max_length=50)),
                ('last_name', models.CharField(default=False, max_length=50)),
                ('amount_collected', models.FloatField(default=0.0)),
                ('receipt_number', models.IntegerField(default=False)),
                ('collection_date', models.DateField(default=False)),
                ('branch_id', models.IntegerField(default=0)),
                ('authorization_status', models.CharField(default='PENDING', max_length=100, null=True)),
                ('authorization_note', models.CharField(default='Not Authorized By Branch Manager', max_length=100, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RM_Daily_Activity',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cilents_collected', models.IntegerField(default=0)),
                ('amount_collected', models.FloatField(default=0.0, null=True)),
                ('new_cilents', models.IntegerField(default=0)),
                ('amount_disbursed', models.FloatField(default=0.0)),
                ('activitydate', models.DateField(default=False)),
                ('before_authorization', models.CharField(default=False, max_length=23)),
                ('after_authorization', models.CharField(default=False, max_length=23)),
                ('authorization_note', models.CharField(default='Not Authorized By Branch Manager', max_length=100)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RM_Weekly_Customers',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('from_date', models.DateField(default=False)),
                ('to_date', models.DateField(default=False)),
                ('customer_category', models.CharField(default=False, max_length=50)),
                ('number_customers', models.IntegerField(default=0)),
                ('before_authorization', models.CharField(default=False, max_length=23, null=True)),
                ('after_authorization', models.CharField(default=False, max_length=23, null=True)),
                ('authorization_note', models.CharField(default='Not Authorized By Branch Manager', max_length=100, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RM_Weekly_Customers_Portfolio',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('from_date', models.DateField(default=False)),
                ('to_date', models.DateField(default=False)),
                ('day_category', models.CharField(default=False, max_length=50)),
                ('portfolio_clients', models.IntegerField(default=0)),
                ('portfolio_amount', models.FloatField(default=0.0)),
                ('before_authorization', models.CharField(default=False, max_length=23, null=True)),
                ('after_authorization', models.CharField(default=False, max_length=23, null=True)),
                ('authorization_note', models.CharField(default='Not Authorized By Branch Manager', max_length=100, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Targets_Collections_Disbursement',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('collections', models.FloatField(default=0.0)),
                ('disbursements', models.FloatField(default=0.0)),
                ('new_customers', models.FloatField(default=0.0)),
                ('rm_id', models.IntegerField(default=False)),
                ('active_portfoilo', models.FloatField(default=0.0)),
                ('bad_portfoilo', models.FloatField(default=0.0)),
                ('from_date', models.DateField(default=False)),
                ('to_date', models.DateField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Targets_Portfoilo',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('rm_id', models.IntegerField(default=False)),
                ('active_portfoilo', models.FloatField(default=0.0)),
                ('bad_portfoilo', models.FloatField(default=0.0)),
                ('from_date', models.DateField(default=False)),
                ('to_date', models.DateField(default=False)),
                ('day_category', models.CharField(default=False, max_length=50)),
                ('number_cilents', models.IntegerField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
            ],
        ),
        #migrations.CreateModel(
        #     name='Profile',
        #     fields=[
        #         ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        #         ('location', models.CharField(default=False, max_length=100)),
        #         ('created_on', models.DateField(default=False)),
        #         ('created_by', models.IntegerField(default=False)),
        #         ('update_on', models.DateTimeField(auto_now=True, null=True)),
        #         ('updated_by', models.IntegerField(default=False, null=True)),
        #         ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Branch')),
        #         ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
        #     ],
        # ),
        migrations.CreateModel(
            name='Disbursements',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount_disbursed', models.FloatField(default=0.0)),
                ('branch_id', models.IntegerField(default=False)),
                ('disbursed_date', models.DateField(default=False)),
                ('id_number', models.IntegerField(default=0.0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
                ('customer_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Potential_Customers')),
            ],
        ),
    ]
