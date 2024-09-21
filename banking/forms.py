from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomSignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

from django import forms

class PinForm(forms.Form):
    pin = forms.CharField(widget=forms.PasswordInput(), max_length=4, min_length=4, required=True)
    confirm_pin = forms.CharField(widget=forms.PasswordInput(), max_length=4, min_length=4, required=True)

    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        if not pin.isdigit():
            raise forms.ValidationError("PIN must be numeric.")
        return pin
