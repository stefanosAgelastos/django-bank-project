from __future__ import annotations
from decimal import Decimal
from django.conf import settings
from django.db import models, transaction
from django.db.models import Q
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from .errors import InsufficientFunds
from enum import Enum


class UID(models.Model):
    @classmethod
    @property
    def uid(cls):
        return cls.objects.create()

    def __str__(self):
        return f'{self.pk}'


class Rank(models.Model):
    name = models.CharField(max_length=35, unique=True, db_index=True)
    value = models.IntegerField(unique=True, db_index=True)

    @classmethod
    def default_rank(cls) -> Rank:
        return cls.objects.all().aggregate(models.Min('value'))['value__min']

    def __str__(self):
        return f'{self.value}:{self.name}'


class Customer(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.PROTECT)
    rank = models.ForeignKey(Rank, default=2, on_delete=models.PROTECT)
    personal_id = models.IntegerField(db_index=True)
    phone = models.CharField(max_length=35, db_index=True)

    @property
    def full_name(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def accounts(self) -> QuerySet:
        return Account.objects.filter(user=self.user)

    @property
    def can_make_loan(self) -> bool:
        return self.rank.value >= settings.CUSTOMER_RANK_LOAN

    @property
    def default_account(self) -> Account:
        return Account.objects.filter(user=self.user).first()

    def make_loan(self, amount, name):
        assert self.can_make_loan, 'User rank does not allow for making loans.'
        assert amount >= 0, 'Negative amount not allowed for loan.'
        loan = Account.objects.create(user=self.user, name=f'Loan: {name}')
        Ledger.transfer(
            amount,
            loan,
            f'Loan paid out to account {self.default_account}',
            self.default_account,
            f'Credit from loan {loan.pk}: {loan.name}',
            is_loan=True
        )

    @classmethod
    def search(cls, search_term):
        return cls.objects.filter(
            Q(user__username__contains=search_term) |
            Q(user__first_name__contains=search_term) |
            Q(user__last_name__contains=search_term) |
            Q(user__email__contains=search_term) |
            Q(personal_id__contains=search_term) |
            Q(phone__contains=search_term)
        )[:15]

    def __str__(self):
        return f'{self.personal_id}: {self.full_name}'


class MFA:
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mfa_token = models.SmallIntegerField(db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, db_index=True)

    class Meta:
        get_latest_by = 'pk'

    @property
    def movements(self) -> QuerySet:
        return Ledger.objects.filter(account=self)

    @property
    def balance(self) -> Decimal:
        return self.movements.aggregate(models.Sum('amount'))['amount__sum'] or Decimal(0)

    def __str__(self):
        return f'{self.pk} :: {self.user} :: {self.name} :: {self.balance}'


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    cvv = models.SmallIntegerField(db_index=True)
    number = models.IntegerField(db_index=True)
    password = models.SmallIntegerField(db_index=True)
    expires_At = models.DateTimeField(db_index=True)


class Ledger(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    transaction = models.ForeignKey(UID, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    text = models.TextField()

    @classmethod
    def transfer(cls, amount, debit_account, debit_text, credit_account, credit_text, is_loan=False) -> int:
        assert amount >= 0, 'Negative amount not allowed for transfer.'
        with transaction.atomic():
            if debit_account.balance >= amount or is_loan:
                uid = UID.uid
                cls(amount=-amount, transaction=uid,
                    account=debit_account, text=debit_text).save()
                cls(amount=amount, transaction=uid,
                    account=credit_account, text=credit_text).save()
            else:
                raise InsufficientFunds
        return uid

    def __str__(self):
        return f'{self.amount} :: {self.transaction} :: {self.timestamp} :: {self.account} :: {self.text}'


class ExternalTransactionStatus(Enum):
    C = 'Created'
    V = 'Validated'


class External_Ledger(models.Model):
    our_transaction = models.ForeignKey(Ledger, on_delete=models.PROTECT)
    ext_transaction = models.IntegerField(db_index=True)
    status = models.CharField(max_length=2, choices=[(
        x, x.value) for x in ExternalTransactionStatus], default=ExternalTransactionStatus.C)

    @classmethod
    def transfer(cls, amount, external_bank, ext_uid, external_bank_account, customer_account, recipient_text) -> int:
        assert amount >= 0, 'Negative amount not allowed for transfer.'
        with transaction.atomic():
            try:
                our_uid = Ledger.transfer(
                    amount, external_bank_account,  f'TRANSFER RECIPIENT: {customer_account}', customer_account, f'TRANSFER FROM: {external_bank} TEXT: {recipient_text}')
            except InsufficientFunds:
                raise
            else:
                cls.save(our_transaction=our_uid, ext_transaction=ext_uid)
        return our_uid

    @classmethod
    def confirm_transfer(cls, ext_uid):
        try:
            ext_tran = cls.objects.get(ext_transaction=ext_uid)
        except External_Ledger.DoesNotExist:
            raise
        else:
            ext_tran.update(status=ExternalTransactionStatus.V)
