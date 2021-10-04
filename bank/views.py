from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Account


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
def details(request, pk):
    assert not request.user.is_staff, 'Staff user routing customer view.'

    account = get_object_or_404(Account, user=request.user, pk=pk)

    context = {
        'account': pk,
        'movements': account.movements,
        'balance': account.balance
    }
    return render(request, 'bank/details.html', context)


# Staff views

@login_required
def staff_dashboard(request):
    assert request.user.is_staff, 'Customer user routing staff view.'
    context = {}
    return render(request, 'bank/staff_dashboard.html', context)
