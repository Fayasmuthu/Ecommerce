from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', 'first_name', 'last_name', 'email', 'phone_number']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
            'first_name': forms.TextInput(attrs={'class': "form-control", 'id': "account-fn"}),
            'last_name': forms.TextInput(attrs={'class': "form-control", 'id': "account-ln"}),
            'email': forms.EmailInput(attrs={'class': "form-control", 'id': "account-email", 'readonly': 'readonly'}),
            'phone_number': forms.TextInput(attrs={'class': "form-control", 'id': "account-phone"}),
        }
