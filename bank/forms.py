from django import forms


class ProfileForm(forms.Form):
    first_name  = forms.CharField(label='First Name', max_length=35)
    last_name   = forms.CharField(label='Last Name', max_length=35)
    personal_id = forms.IntegerField(label='Personal ID Number')
    phone       = forms.CharField(label='Phone Number', max_length=35)
    email       = forms.EmailField(label='Email Address')
