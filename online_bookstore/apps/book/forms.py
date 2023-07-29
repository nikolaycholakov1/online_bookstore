# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from online_bookstore.apps.book.models import BookReview, Customer


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Customer
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


class ShippingInfoForm(forms.Form):
    delivery_address = forms.CharField()
    city = forms.CharField(max_length=30)
    zip_code = forms.CharField(max_length=9)
    country = forms.CharField(max_length=30)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'age', 'profile_picture', 'delivery_address']
        widgets = {
            'delivery_address': forms.Textarea(attrs={'rows': 3, 'cols': 32}),
        }
