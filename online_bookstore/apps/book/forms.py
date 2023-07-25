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