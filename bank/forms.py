from django import forms
from django.contrib.auth.models import User
from .models import Customer


class TransferForm(forms.Form):
    amount  = forms.DecimalField(label='Amount', max_digits=10)
    debit_account = forms.ModelChoiceField(label='Debit Account', queryset=Customer.objects.none())
    debit_text = forms.CharField(label='Debit Account Text', max_length=25)
    credit_account = forms.IntegerField(label='Credit Account Number')
    credit_text = forms.CharField(label='Credit Account Text', max_length=25)

