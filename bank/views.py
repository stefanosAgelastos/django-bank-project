from decimal import Decimal
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TransferForm
from .models import Account, Ledger
from .errors import InsufficientFunds


@login_required
def index(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('bank:staff_dashboard'))
    else:
        return HttpResponseRedirect(reverse('bank:dashboard'))


# Customer views

@login_required
def dashboard(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    accounts = request.user.customer.accounts
    context = {
        'accounts': accounts,
    }
    return render(request, 'bank/dashboard.html', context)


@login_required
def account_details(request, pk):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    account = get_object_or_404(Account, user=request.user, pk=pk)
    context = {
        'account': account,
        'movements': account.movements,
        'balance': account.balance
    }
    return render(request, 'bank/account_details.html', context)


@login_required
def transaction_details(request, transaction):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    movements = Ledger.objects.filter(transaction=transaction)
    context = {
        'movements': movements,
    }
    return render(request, 'bank/transaction_details.html', context)


@login_required
def make_transfer(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    if request.method == 'POST':
        form = TransferForm(request.POST)
        form.fields['debit_account'].queryset = request.user.customer.accounts
        if form.is_valid():
            amount = form.cleaned_data['amount']
            debit_account = Account.objects.get(pk=form.cleaned_data['debit_account'].pk)
            debit_text = form.cleaned_data['debit_text']
            credit_account = Account.objects.get(pk=form.cleaned_data['credit_account'])
            credit_text = form.cleaned_data['credit_text']
            try:
                Ledger.transfer(amount, debit_account, debit_text, credit_account, credit_text)
                return HttpResponseRedirect(reverse('bank:index'))
            except InsufficientFunds:
                return render(request, 'bank/reject_transfer.html', {})
    else:
        form = TransferForm()
    form.fields['debit_account'].queryset = request.user.customer.accounts
    context = {
        'form': form,
    }
    return render(request, 'bank/make_transfer.html', context)


@login_required
def make_loan(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    if not request.user.customer.can_make_loan:
        return render(request, 'bank/reject_loan.html', {})
    if request.method == 'POST':
        request.user.customer.make_loan(Decimal(request.POST['amount']), request.POST['name'])
        return HttpResponseRedirect(reverse('bank:dashboard'))
    return render(request, 'bank/make_loan.html', {})


# Staff views

@login_required
def staff_dashboard(request):
    assert request.user.is_staff, 'Customer user routing staff view.'
    context = {}
    return render(request, 'bank/staff_dashboard.html', context)
