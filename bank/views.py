from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, CustomerProfileForm, UserForm
from .models import Customer


@login_required
def index(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('bank:staff_dashboard'))
    else:
        return HttpResponseRedirect(reverse('bank:dashboard'))


@login_required
def dashboard(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'
    context = {}
    return render(request, 'bank/dashboard.html', context)


@login_required
def staff_index(request):
    assert request.user.is_staff, 'Customer user routing staff view.'
    context = {}
    return render(request, 'bank/staff_index.html', context)
