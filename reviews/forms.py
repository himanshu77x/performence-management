from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    review_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Review
        fields = ['title', 'employee', 'review_date', 'review_period', 'rating', 'comment']
