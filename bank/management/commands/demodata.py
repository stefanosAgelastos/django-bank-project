import secrets
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bank.models import Account, Ledger, Customer
from transfers.models import Entity


class Command(BaseCommand):
    def handle(self, **options):
        print('Adding demo data ...')

        admin = User.objects.create_superuser(
            'admin', 'admin@example.com', 'adminpass')
        admin.save()

        bank_user = User.objects.create_user(
            'bank', email='', password=secrets.token_urlsafe(64))
        bank_user.is_active = False
        bank_user.save()
        ipo_account = Account.objects.create(
            user=bank_user, name='Bank IPO Account')
        ops_account = Account.objects.create(
            user=bank_user, name='Bank OPS Account')
        Ledger.transfer(
            10_000_000,
            ipo_account,
            'Operational Credit',
            ops_account,
            'Operational Credit',
            is_loan=True
        )

        dummy_user = User.objects.create_user(
            'dummy', email='dummy@dummy.com', password='mirror12')
        dummy_user.first_name = 'Dummy'
        dummy_user.last_name = 'Dimwit'
        dummy_user.save()
        dummy_customer = Customer(
            user=dummy_user, personal_id='555666', phone='555666')
        dummy_customer.save()
        dummy_account = Account.objects.create(
            user=dummy_user, name='Checking account')
        dummy_account.save()
        Ledger.transfer(
            1_000,
            ops_account,
            'Payout to dummy',
            dummy_account,
            'Payout from bank'
        )

        john_user = User.objects.create_user(
            'john', email='john@smith.com', password='mirror12')
        john_user.first_name = 'John'
        john_user.last_name = 'Smith'
        john_user.save()
        john_customer = Customer.objects.create(
            user=john_user, personal_id='666777', phone='666777')
        john_customer.save()
        john_account = Account.objects.create(
            user=john_user, name='Checking account')
        john_account.save()

        bankia_user = User.objects.create_user(
            'bankia_manager', email='mgmt@bankia.com', password='bankia12')
        bankia_user.save()
        bankia_entity = Entity.objects.create(
            user=bankia_user, personal_id='121212',  phone='121212', brand='Bankia AS', type=Entity.EntityType.NATIONAL_BANK)
        bankia_entity.save()
        bankia_account = Account.objects.create(
            user=bankia_user, name='The account')
        bankia_account.save()
        Ledger.transfer(
            1_000,
            ops_account,
            'Payout to Bankia',
            bankia_account,
            'Payout from bank'
        )
