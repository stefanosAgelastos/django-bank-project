from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('bank:index_teller'))
    else:
        return HttpResponseRedirect(reverse('bank:index_customer'))


@login_required
def index_customer(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'
    context = {}
    return render(request, 'bank/index.html', context)


@login_required
def index_teller(request):
    assert request.user.is_staff, 'Customer user routing staff view.'
    context = {}
    return render(request, 'bank/index.html', context)
