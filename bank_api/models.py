from django.db import models, transaction
from enum import Enum
from bank.models import Ledger, Customer
from bank.errors import InsufficientFunds


class ExternalTransactionStatus(Enum):
    C = 'Created'
    V = 'Validated'


class ExternalLedger(Ledger):

    class Meta:
        db_table = "external_ledger"

    reference = models.IntegerField(db_index=True, default=-1)
    status = models.CharField(max_length=2, choices=[(
        x, x.value) for x in ExternalTransactionStatus], default=ExternalTransactionStatus.C)

    @classmethod
    def transfer(cls, amount, external_bank, ext_ref, creditor_account, recipient_account, recipient_text) -> int:
        assert amount >= 0, 'Negative amount not allowed for transfer.'
        with transaction.atomic():
            try:
                uid = super().transfer(
                    amount, creditor_account,
                    f'TRANSFER RECIPIENT: {recipient_account}',
                    recipient_account,
                    f'TRANSFER FROM: {external_bank} TEXT: {recipient_text}'
                )
            except InsufficientFunds:
                raise
            else:
                cls.objects.filter(transaction_id=uid).update(
                    reference=ext_ref)
        return uid

    # @classmethod
    # def confirm_transfer(cls, ext_ref):
    #     try:
    #         ext_tran = cls.objects.get(reference=ext_ref)
    #     except ExternalLedger.DoesNotExist:
    #         raise
    #     else:
    #         ext_tran.update(status=ExternalTransactionStatus.V)


class EntityType(Enum):
    NB = 'National Bank'
    FB = 'Foreign Bank'
    C = 'Card'


class Entity(Customer):

    class Meta:
        verbose_name_plural = "Entities"

    api_url = models.CharField(
        max_length=50, blank=True, null=True)
    api_username = models.CharField(
        max_length=50, blank=True, null=True)
    api_password = models.CharField(
        max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=50)
    type = models.CharField(max_length=2, choices=[(
        x, x.value) for x in EntityType])
