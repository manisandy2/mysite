from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _

from django import forms
from django.core.exceptions import ValidationError

from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class': 'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('id','Full_Name','Gender','Marital_Status','Mother_Tongue','Mobile_No','email', 'password1','password2')

        widgets = {
            "Full_Name": forms.TextInput(attrs={'class': 'form-control'}),
            "Gender": forms.Select(attrs={'class': 'form-control'}),
            "Marital_Status": forms.Select(attrs={'class': 'form-control'}),
            "Mother_Tongue": forms.Select(attrs={'class':'form-control'}),
            "Mobile_No": forms.NumberInput(attrs={'class':'form-control'}),
            "email": forms.EmailInput(attrs={'class':'form-control'}),
            "password1": forms.PasswordInput(attrs={'class':'form-control'}),
            "password2": forms.PasswordInput(attrs={'class':'form-control'}),

        }

