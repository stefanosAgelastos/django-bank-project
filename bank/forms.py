from django import forms
from django.contrib.auth.models import User
from .models import Customer


class ProfileForm(forms.Form):
    first_name  = forms.CharField(label='First Name', max_length=35)
    last_name   = forms.CharField(label='Last Name', max_length=35)
    personal_id = forms.IntegerField(label='Personal ID Number')
    phone       = forms.CharField(label='Phone Number', max_length=35)
    email       = forms.EmailField(label='Email Address')


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['personal_id', 'phone']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
