from django import forms
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1.0, '1.0'),
        (1.5, '1.5'),
        (2.0, '2.0'),
        (2.5, '2.5'),
        (3.0, '3.0'),
        (3.5, '3.5'),
        (4.0, '4.0'),
        (4.5, '4.5'),
        (5.0, '5.0'),
    ]

    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select)

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }