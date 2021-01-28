# Generated by Django 2.2.10 on 2021-01-26 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20210116_2307'),
    ]

    operations = [
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
    ]