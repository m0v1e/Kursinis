from .models import CarReview, Profilis
from django import forms
from django.contrib.auth.models import User

class CarReviewForm(forms.ModelForm):
    class Meta:
        model = CarReview
        fields = ('comment', 'car', 'owner',)
        widgets = {'car': forms.HiddenInput(), 'owner': forms.HiddenInput()}

