from django import forms
from .models import Club, ClubRole, ClubMembership
from events.forms import StyledFormMixin


class ClubForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter club name'}),
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your club'}),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'created_at': forms.SelectDateWidget(), 
        }


class ClubRoleForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ClubRole
        fields = ['club', 'role_name']
        widgets = {
            'club': forms.Select(),
            'role_name': forms.TextInput(attrs={'placeholder': 'e.g. President, Secretary, Member'}),
        }


class ClubMembershipForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = ClubMembership
        fields = ['user', 'club', 'role']
        widgets = {
            'user': forms.Select(),
            'club': forms.Select(),
            'role': forms.Select(),
        }
