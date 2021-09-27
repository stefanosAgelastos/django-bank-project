from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Customer


@login_required
def index(request):
    if request.user.is_staff:
        return HttpResponseRedirect(reverse('bank:index_teller'))
    else:
        try:
            request.user.customer
            return HttpResponseRedirect(reverse('bank:index_customer'))
        except: # Customer.RelatedObjectDoesNotExist:
            return HttpResponseRedirect(reverse('bank:profile_customer'))


@login_required
def index_customer(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'
    context = {}
    return render(request, 'bank/index.html', context)


@login_required
def profile_customer(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'
    context = {}
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name  = form.cleaned_data['last_name']
            user.email      = form.cleaned_data['email']
            user.save()
            customer = Customer()
            customer.personal_id    = form.cleaned_data['personal_id']
            customer.phone          = form.cleaned_data['phone']
            customer.save()
            context['status'] = 'Profile updated successfully.'
        else:
            context['error'] = form.error

    form = ProfileForm()
    form.first_name     = request.user.first_name
    form.last_name      = request.user.last_name
    form.email          = request.user.email


    context['form'] = form
    return render(request, 'bank/profile.html', context)


@login_required
def index_teller(request):
    assert request.user.is_staff, 'Customer user routing staff view.'
    context = {}
    return render(request, 'bank/index.html', context)
