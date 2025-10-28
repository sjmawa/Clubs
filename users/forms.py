import re
from django.contrib.auth.models import User,Group,Permission
from django import forms
from events.forms import StyledFormMixin
from django.contrib.auth.forms import AuthenticationForm
from clubs.models import ClubRole as clubrole

class CustomRegisterForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model= User
        fields= ['username', 'first_name', 'last_name', 'email', 'password1', 'confirm_password']
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors =[]
        if len(password1) < 8:
            errors.append('Password must be at least 8 character long')
        if not re.search(r'[A-Z]', password1):
            errors.append(
                'Password must include at least one uppercase letter.')
        if not re.search(r'[a-z]', password1):
            errors.append(
                'Password must include at least one lowercase letter.')
        if not re.search(r'[0-9]', password1):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', password1):
            errors.append(
                'Password must include at least one special character.')
        if errors:
            raise forms.ValidationError(errors)
        return password1
    def clean_email(self):
        email= self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email
    # non field error
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("confirm_password")
        
        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data        
"""
custom login form
"""
class LoginForm(StyledFormMixin , AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=clubrole.objects.all(),
        empty_label="Select a Role"
    )
class CreateRoleForm(StyledFormMixin, forms.ModelForm):
    permissions= forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget= forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )
    class Meta:
        model = Group
        fields= ['name','permissions']