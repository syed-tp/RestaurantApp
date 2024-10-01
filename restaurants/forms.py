from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1.0, 'max': 5.0, 'step': 0.1}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }