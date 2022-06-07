from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from .forms import TransferForm
from bank.models import Account
from bank.errors import InsufficientFunds
from .models import ExternalLedger


@login_required
def make_transfer(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    if request.method == 'POST':
        form = TransferForm(request.POST)
        form.fields['debit_account'].queryset = request.user.customer.accounts
        if form.is_valid():
            amount = form.cleaned_data['amount']
            debit_account = Account.objects.get(
                pk=form.cleaned_data['debit_account'].pk)
            debit_text = form.cleaned_data['debit_text']
            external_entity = form.cleaned_data['external_entity']
            recipient_account = Account.objects.get(
                pk=form.cleaned_data['recipient_account'])
            recipient_text = form.cleaned_data['recipient_text']
            try:
                transfer_uid = ExternalLedger.send_transfer(
                    amount,
                    external_entity,
                    debit_account,
                    debit_text,
                    recipient_account,
                    recipient_text)
                return render(request, 'transfer_progress.html', {'transfer_uid': transfer_uid})
            except InsufficientFunds:
                context = {
                    'title': 'Transfer Error',
                    'error': 'Insufficient funds for transfer.'
                }
                return render(request, 'bank/error.html', context)
    else:
        form = TransferForm()
    form.fields['debit_account'].queryset = request.user.customer.accounts
    context = {
        'form': form,
    }
    return render(request, 'make_transfer.html', context)


@login_required
def transfer_status(request, transfer_uid):
    transfer = ExternalLedger.objects.filter(
        transaction_id=transfer_uid).first()
    if not request.user.is_staff:
        if not transfer.account.user == request.user:
            raise PermissionDenied('Customer is not part of the transaction.')
    context = {
        'transfer_uid': transfer_uid,
    }
    if not transfer.status == ExternalLedger.ExternalTransactionStatus.VALIDATED:
        return render(request, 'transfer_status.html', context)
    elif transfer.status == ExternalLedger.ExternalTransactionStatus.FAILED:
        context = {
            'title': 'Transfer Confirmation Error',
            'error': 'The issue has been forwarded to a human.'
        }
        return render(request, 'bank/error.html', context)
    else:
        return transfer_details(request, transfer_uid)


@login_required
def transfer_details(request, transaction):
    movements = ExternalLedger.objects.filter(transaction=transaction)
    if not request.user.is_staff:
        if not movements.filter(account__in=request.user.customer.accounts):
            raise PermissionDenied('Customer is not part of the transaction.')
    context = {
        'movements': movements,
    }
    return render(request, 'bank/transfer_details.html', context)
