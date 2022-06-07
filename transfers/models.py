from django.db import models, transaction
from bank.models import ExternalTransactionStatus, Ledger, Customer
from bank.errors import InsufficientFunds
from .apps import BankApiConfig
from .utils import check_account


class ExternalLedger(Ledger):
    class ExternalTransactionStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        CREATED = 'C', 'Created'
        VALIDATED = 'V', 'Validated'
        FAILED = 'F', 'Failed'

    class Meta:
        db_table = f'{BankApiConfig.name}_external_ledger'

    reference = models.IntegerField(db_index=True, default=-1)
    status = models.CharField(max_length=1,
                              choices=ExternalTransactionStatus.choices,
                              default=ExternalTransactionStatus.CREATED)

    @classmethod
    def receive_transfer(cls, amount, reference, entity, recipient_account, recipient_text) -> int:
        assert amount >= 0, 'Negative amount not allowed for transfer.'
        with transaction.atomic():
            try:
                uid = super().transfer(
                    amount, entity.default_account,
                    f'TRANSFER RECIPIENT: {recipient_account}',
                    recipient_account,
                    f'TRANSFER FROM: {entity.brand} | TEXT: {recipient_text}'
                )
            except InsufficientFunds:
                raise
            else:
                cls.objects.filter(transaction_id=uid).update(
                    reference=reference)
                return {'transaction': uid.__str__}

    @classmethod
    def send_transfer(cls, amount, entity, sender_account, sender_text, recipient_account, recipient_text) -> int:
        assert amount >= 0, 'Negative amount not allowed for transfer.'
        with transaction.atomic():
            try:
                uid = super().transfer(
                    amount,
                    sender_account,
                    f'TRANSFER TO: {entity.brand}:{recipient_account} | TEXT: {sender_text}',
                    entity.default_account,
                    f'TRANSFER RECIPIENT: {recipient_account}',
                )
            except InsufficientFunds:
                raise
            else:
                cls.objects.filter(transaction_id=uid).update(
                    status=cls.ExternalTransactionStatus.PENDING)
                return uid

    @classmethod
    def reference_exists(cls, reference, entity) -> bool:
        try:
            ExternalLedger.objects.get(
                reference=reference, account=entity.default_account)
        except ExternalLedger.DoesNotExist:
            return False
        except ExternalLedger.MultipleObjectsReturned:
            return True
        else:
            return True
    # @classmethod
    # def confirm_transfer(cls, reference):
    #     try:
    #         ext_tran = cls.objects.get(reference=reference)
    #     except ExternalLedger.DoesNotExist:
    #         raise
    #     else:
    #         ext_tran.update(status=ExternalTransactionStatus.V)


class Entity(Customer):

    class EntityType(models.TextChoices):
        NATIONAL_BANK = 'NB', 'National Bank'
        FOREIGN_BANK = 'FB', 'Foreign Bank'
        CARD_ISSUER = 'CI', 'Card Issuer'

    class Meta:
        verbose_name_plural = "Entities"

    api_url = models.CharField(
        max_length=50, blank=True, null=True)
    api_username = models.CharField(
        max_length=50, blank=True, null=True)
    api_password = models.CharField(
        max_length=50, blank=True, null=True)
    brand = models.CharField(max_length=50)
    type = models.CharField(max_length=2, choices=EntityType.choices)

    def check_account_id(self, account_id) -> bool:
        try:
            return check_account(self, account_id)
        except:
            raise

    def __str__(self):
        return f'{self.brand}'
