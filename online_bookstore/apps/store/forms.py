# store/forms.py

from django import forms


class CheckoutForm(forms.Form):
    shipping_full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    shipping_country = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_address = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    shipping_zipcode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    payment_method = forms.ChoiceField(label='Payment Method', choices=(
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ))
    agree_to_terms = forms.BooleanField(
        label='I agree to the terms and conditions',
        required=True
    )
