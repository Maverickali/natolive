# Generated by Django 2.2.10 on 2021-04-03 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ids',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('account_number', models.CharField(max_length=100)),
                ('id_number', models.CharField(max_length=100, null=True)),
                ('id_status', models.CharField(default='submitted', max_length=100)),
                ('id_loan_count', models.IntegerField(default=False, null=True)),
                ('branch_id_holder', models.IntegerField(default=1)),
                ('id_override_status', models.CharField(default='no', max_length=50)),
                ('id_override_reason', models.CharField(default=False, max_length=200)),
                ('resubmission_date', models.DateField(default=False, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.IntegerField(default=False, null=True)),
                ('branch_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Branch')),
                ('customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Potential_Customers')),
            ],
        ),
    ]
