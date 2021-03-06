# Generated by Django 3.2.7 on 2022-06-06 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bank', '0008_external_ledger_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('customer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bank.customer')),
                ('api_url', models.CharField(blank=True, max_length=50, null=True)),
                ('api_username', models.CharField(blank=True, max_length=50, null=True)),
                ('api_password', models.CharField(blank=True, max_length=50, null=True)),
                ('brand', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('NB', 'National Bank'), ('FB', 'Foreign Bank'), ('CI', 'Card Issuer')], max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Entities',
            },
            bases=('bank.customer',),
        ),
        migrations.CreateModel(
            name='ExternalLedger',
            fields=[
                ('ledger_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bank.ledger')),
                ('reference', models.IntegerField(db_index=True, default=-1)),
                ('status', models.CharField(choices=[('P', 'Pending'), ('C', 'Created'), ('V', 'Validated')], default='C', max_length=1)),
            ],
            options={
                'db_table': 'transfers_external_ledger',
            },
            bases=('bank.ledger',),
        ),
    ]
