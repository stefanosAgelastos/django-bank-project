from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, CustomerProfileForm, UserForm
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
    return render(request, 'bank/index_customer.html', context)


@login_required
def profile_customer(request):
    assert not request.user.is_staff, 'Staff user routing customer view.'
    user_form = UserForm(instance=request.user)
    try:
        customer_profile_form = CustomerProfileForm(instance=request.user.customer)
    except:
        customer_profile_form = CustomerProfileForm()

    context = {
        'user_form': user_form,
        'customer_profile_form': customer_profile_form,
    }

    return render(request, 'bank/profile.html', context)


@login_required
def profile_customer_update_user(request):
    pass


@login_required
def profile_customer_update_customer(request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
        form['user'] = request.user
        form.save()
    context = { 'user_profile_form': form }
    return render(request, 'bank/profile_customer_update_customer_partial.html', context)


@login_required
def index_teller(request):
    assert request.user.is_staff, 'Customer user routing staff view.'
    context = {}
    return render(request, 'bank/index_teller.html', context)
