from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Customer, Account, Rank


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


class NewCustomerForm(forms.Form):
    username    = forms.CharField(label='User Name', max_length=25)
    first_name  = forms.CharField(label='First Name', max_length=25)
    last_name   = forms.CharField(label='Last Name', max_length=25)
    personal_id = forms.IntegerField(label='Personal ID')
    email       = forms.EmailField(label='Email Address')
    phone       = forms.CharField(label='Phone Number', max_length=25)
    rank        = forms.ModelChoiceField(label='Customer Rank', queryset=Rank.objects.none())

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username):
            self._errors['username'] = self.error_class(['Username already exists.'])
        return self.cleaned_data


class UserForm(forms.ModelForm):
    username = forms.CharField(label='Username', disabled=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('rank', 'personal_id', 'phone')
