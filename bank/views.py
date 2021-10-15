from decimal import Decimal
from secrets import token_urlsafe
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import TransferForm, NewCustomerForm, UserForm, CustomerForm
from .models import Account, Ledger, Rank, Customer
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
                # TODO: Better to redirect the user to the transaction details
                return HttpResponseRedirect(reverse('bank:index'))
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
    return render(request, 'bank/make_transfer.html', context)


@login_required
def make_loan(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    if not request.user.customer.can_make_loan:
        context = {
            'title': 'Create Loan Error',
            'error': 'Loan could not be completed.'
        }
        return render(request, 'bank/error.html', context)
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


@login_required
def staff_search_partial(request):
    assert request.user.is_staff, 'Customer user routing staff view.'

    search_term = request.POST['search_term']
    customers = Customer.search(search_term)
    context = {
        'customers': customers,
    }
    return render(request, 'bank/staff_search_partial.html', context)


@login_required
def staff_customer_details(request, pk):
    assert request.user.is_staff, 'Customer user routing staff view.'

    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'GET':
        user_form = UserForm(instance=customer.user)
        customer_form = CustomerForm(instance=customer)
    elif request.method == 'POST':
        user_form = UserForm(request.POST, instance=customer.user)
        customer_form = CustomerForm(request.POST, instance=customer)
        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
    context = {
        'customer': customer,
        'user_form': user_form,
        'customer_form': customer_form,
    }
    return render(request, 'bank/staff_customer_details.html', context)


@login_required
def staff_new_customer(request):
    assert request.user.is_staff, 'Customer user routing staff view.'

    if request.method == 'POST':
        form = NewCustomerForm(request.POST)
        form.fields['rank'].queryset = Rank.objects.all()
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            personal_id = form.cleaned_data['personal_id']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            rank = form.cleaned_data['rank']
            try:
                password = token_urlsafe(16)
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                Customer.objects.create(user=user, phone=phone, rank=rank, personal_id=personal_id)
                print(f'****** Username: {username}   Password: {password}')
                # TODO: go to customer details page
            except IntegrityError:
                return render(request, 'bank/error.html', {'title': 'Error', 'error': 'Unknow database error.'})
    else:
        form = NewCustomerForm()
    form.fields['rank'].queryset = Rank.objects.all()
    context = {
        'form': form,
    }
    return render(request, 'bank/staff_new_customer.html', context)
