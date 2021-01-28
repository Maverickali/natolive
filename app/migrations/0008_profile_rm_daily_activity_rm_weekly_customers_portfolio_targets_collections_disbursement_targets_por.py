# Generated by Django 2.2.10 on 2021-01-16 18:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0007_auto_20210103_1123'),
    ]

    operations = [
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
                ('updated_by', models.CharField(max_length=50, null=True)),
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
                ('updated_by', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Targets_Collections_Disbursement',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('Collections', models.FloatField(default=0.0)),
                ('Disbursements', models.FloatField(default=0.0)),
                ('New_Customers', models.FloatField(default=0.0)),
                ('rm_id', models.IntegerField(default=False)),
                ('active_portfoilo', models.FloatField(default=0.0)),
                ('bad_portfoilo', models.FloatField(default=0.0)),
                ('from_date', models.DateField(default=False)),
                ('to_date', models.DateField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.CharField(max_length=50, null=True)),
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
                ('updated_by', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(default=False, max_length=100)),
                ('created_on', models.DateField(default=False)),
                ('created_by', models.IntegerField(default=False)),
                ('update_on', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.CharField(max_length=50, null=True)),
                ('branch_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Branch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]