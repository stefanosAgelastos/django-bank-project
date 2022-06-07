from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Entity
from bank.models import Customer, Account


class TransferForm(forms.Form):
    amount = forms.DecimalField(label='Amount', max_digits=10)
    debit_account = forms.ModelChoiceField(
        label='Debit Account', queryset=Customer.objects.none())
    debit_text = forms.CharField(label='Debit Account Text', max_length=25)
    external_entity = forms.ModelChoiceField(
        label='Other Bank', queryset=Entity.objects.all())
    recipient_account = forms.IntegerField(label='Recipient Account Number')
    recipient_text = forms.CharField(
        label='Recipient Account Text', max_length=25)

    def clean(self):
        super().clean()

        # Ensure positive amount
        if int(self.cleaned_data.get('amount')) < 0:
            self._errors['amount'] = self.error_class(
                ['Amount must be positive.'])

        debit_account = self.cleaned_data.get('debit_account')
        if debit_account.balance < self.cleaned_data.get('amount'):
            self._errors['debit_account'] = self.error_class(
                ['Not enough balance in debit acccount.'])

        # Ensure credit account exist
        recipient_account = self.cleaned_data.get('recipient_account')
        external_entity = self.cleaned_data.get('external_entity')
        if not external_entity.check_account_id(recipient_account):
            self._errors['recipient_account'] = self.error_class(
                ['Recipient account does not exist.'])

        return self.cleaned_data
