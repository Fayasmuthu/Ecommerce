from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':"form-control", 'type':"email", 'required id':"review-email"}))

    class Meta:  # Corrected from 'class meta:'
        model = Review
        fields = ['name','email','rating','review_text']

        widgets = {
            'name': forms.TextInput(attrs={'class':"form-control" ,'type':"text", 'required id':"review-name"}),
            'review_title':forms.TextInput(attrs={'placeholder':'Your Review Title'}),
            'rating': forms.Select(choices=[(i, str(i)) for i in range(1, 6)],attrs={'class':"form-select", 'required id':"review-rating"}),
            'review_text': forms.Textarea(attrs={'rows': 6, 'class':"form-control", 'required id':"review-text"}),
        }
