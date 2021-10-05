import secrets
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bank.models import Account, Ledger, Customer


class Command(BaseCommand):
    def handle(self, **options):
        print('Adding demo data ...')

        bank_user = User.objects.create_user('bank', email='', password=secrets.token_urlsafe(64))
        bank_user.is_active = False
        bank_user.save()
        ipo_account = Account.objects.create(user=bank_user, name='Bank IPO Account')
        ops_account = Account.objects.create(user=bank_user, name='Bank OPS Account')
        Ledger.transfer(
            10_000_000,
            ipo_account,
            'Operational Credit',
            ops_account,
            'Operational Credit',
            is_loan=True
        )

        dummy_user = User.objects.create_user('dummy', email='dummy@dummy.com', password='mirror12')
        dummy_user.first_name = 'Dummy'
        dummy_user.last_name  = 'Dimwit'
        dummy_user.save()
        dummy_customer = Customer(user=dummy_user, personal_id='555666', phone='555666')
        dummy_customer.save()
        dummy_account = Account.objects.create(user=dummy_user, name='Checking account')
        dummy_account.save()

        Ledger.transfer(
            1_000,
            ops_account,
            'Payout to dummy',
            dummy_account,
            'Payout from bank'
        )
