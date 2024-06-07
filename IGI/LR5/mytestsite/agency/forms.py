from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from . import models


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=50, required=True, help_text='Required.')
    address = forms.CharField(max_length=255, required=True, help_text='Required.')
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Required 18+'
    )
    phone_number = forms.CharField(max_length=15, required=True, help_text='Required. Format: +375XXXXXXXXX')

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'address', 'date_of_birth', 'phone_number', 'email', 'password1',
            'password2')

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            raise ValidationError('You must be at least 18 years old to register.')
        return dob


