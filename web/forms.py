from django import forms
from .models import Applicant

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your name'}))
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '@email.com'}))
    phone = forms.CharField(label='Your phone', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter of your Number'}))
    subject = forms.CharField(max_length=100, label='Subject', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Provide short title of your request'}))
    message = forms.CharField(label='Message', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Please describe in detail your request'}))


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['name', 'email', 'message', 'cv']
        widgets = {
            'name': forms.TextInput(attrs={'class':"form-control" ,'placeholder':'Your name','required': True}),
            'email':forms.EmailInput(attrs={'class':"form-control" ,'placeholder':'Your email','required': True}),
            'message':forms.Textarea(attrs={'rows': 6, 'class':"form-control" ,'placeholder':'Message','required': True}),
            'cv': forms.FileInput(attrs={'class':"form-control" ,'type':"file"}),
        }

    
