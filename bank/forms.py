from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import Customer, Account


class TransferForm(forms.Form):
    amount  = forms.DecimalField(label='Amount', max_digits=10)
    debit_account = forms.ModelChoiceField(label='Debit Account', queryset=Customer.objects.none())
    debit_text = forms.CharField(label='Debit Account Text', max_length=25)
    credit_account = forms.IntegerField(label='Credit Account Number')
    credit_text = forms.CharField(label='Credit Account Text', max_length=25)

    def clean(self):
        super().clean()
        credit_account = self.cleaned_data.get('credit_account')
        try:
            Account.objects.get(pk=credit_account)
        except ObjectDoesNotExist:
            self._errors['credit_account'] = self.error_class(['Credit account does not exist.'])
        return self.cleaned_data
