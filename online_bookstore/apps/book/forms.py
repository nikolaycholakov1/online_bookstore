# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from online_bookstore.apps.book.models import BookReview


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['review_text']
        labels = {
            'review_text': 'Write your review here:'
        }
        widgets = {
            'review_text': forms.Textarea(attrs={'style': 'min-width: 0;'}),
        }


class OrderForm(forms.Form):
    pk = forms.IntegerField(widget=forms.HiddenInput)
    quantity = forms.IntegerField(initial=1)
    delivery_address = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
    city = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'required': True}))
